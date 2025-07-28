import logging
from datetime import datetime, timedelta

from .models import (
    db,
    UserProfile as ProfileModel,
    VerificationAuditLog,
    KYCRecord,
    AMLLogEntry,
)
from .veriff_service import create_verification_session

MAX_DAILY_TXN_LIMIT = 1000  # AUD
MAX_SINGLE_TXN_LIMIT = 300  # AUD soft flag threshold
MAX_BALANCE_LIMIT = 750  # AUD soft warning before hard KYC at 1000


class UserProfile:
    """Ephemeral profile that mirrors persisted verification data."""

    def __init__(self, user_id: int, db_profile: ProfileModel):
        self.user_id = user_id
        self.db_profile = db_profile
        self.kyc_status = db_profile.verification_status
        self.daily_total = db_profile.daily_total or 0.0
        self.weekly_total = db_profile.weekly_total or 0.0
        self.card_balances: list[tuple[int, float]] = []
        self.txn_log: list[tuple[float, str, list, datetime]] = []
        self.flagged = db_profile.flagged
        self._day = db_profile.day or datetime.utcnow().date()
        self._week_start = db_profile.week_start or (
            self._day - timedelta(days=self._day.weekday())
        )


def get_user_profile(user_id: int) -> UserProfile:
    db_profile = db.session.get(ProfileModel, user_id)
    if not db_profile:
        db_profile = ProfileModel(user_id=user_id)
        db.session.add(db_profile)
        db.session.commit()
    profile = UserProfile(user_id, db_profile)
    return profile


def _reset_totals_if_needed(user: UserProfile) -> None:
    today = datetime.utcnow().date()
    if user._day != today:
        user._day = today
        user.daily_total = 0.0
    week_start = today - timedelta(days=today.weekday())
    if user._week_start != week_start:
        user._week_start = week_start
        user.weekly_total = 0.0
    user.db_profile.day = user._day
    user.db_profile.week_start = user._week_start
    user.db_profile.daily_total = user.daily_total
    user.db_profile.weekly_total = user.weekly_total


def process_transaction(user: UserProfile, amount: float, merchant_id: str, source_cards: list):
    _reset_totals_if_needed(user)

    if amount > MAX_SINGLE_TXN_LIMIT:
        flag_suspicious(user, reason="Single transaction exceeds soft threshold")

    user.daily_total += amount
    user.weekly_total += amount
    user.db_profile.daily_total = user.daily_total
    user.db_profile.weekly_total = user.weekly_total
    user.db_profile.day = user._day
    user.db_profile.week_start = user._week_start
    user.txn_log.append((amount, merchant_id, source_cards, datetime.utcnow()))

    total_consolidated = sum(balance for _, balance in user.card_balances)
    if total_consolidated > MAX_BALANCE_LIMIT:
        warn_user(user, message="Balance approaching AML threshold")

    if total_consolidated >= MAX_DAILY_TXN_LIMIT or user.weekly_total >= MAX_DAILY_TXN_LIMIT:
        trigger_kyc(user, reason="Exceeded AML transaction threshold")

    if detect_structuring(user):
        flag_suspicious(user, reason="Suspected structuring to avoid AML triggers")

    db.session.add(user.db_profile)
    db.session.commit()


def trigger_kyc(user: UserProfile, reason: str):
    if user.kyc_status != "verified":
        user.kyc_status = "pending"
        user.db_profile.verification_status = "pending"
        db.session.add(VerificationAuditLog(user_id=user.user_id, action="kyc_triggered", details=reason))
        db.session.commit()
        send_kyc_request(user, reason)
        store_kyc_information(user.user_id, "kyc_trigger", reason)


def detect_structuring(user: UserProfile) -> bool:
    txns = user.txn_log[-5:]
    if len(txns) >= 5 and all(t[0] < MAX_SINGLE_TXN_LIMIT for t in txns) and sum(t[0] for t in txns) > MAX_DAILY_TXN_LIMIT:
        return True
    return False


def flag_suspicious(user: UserProfile, reason: str):
    user.flagged = True
    user.db_profile.flagged = True
    db.session.add(VerificationAuditLog(user_id=user.user_id, action="flagged", details=reason))
    db.session.commit()
    store_kyc_information(user.user_id, "flagged", reason)
    submit_au_strac_smr(user, reason)


# Stubbed integration hooks -----------------------------------------------

def send_kyc_request(user: UserProfile, reason: str) -> None:
    log(f"KYC request triggered for {user.user_id}: {reason}")
    try:
        session_id = create_verification_session(user.user_id)
        user.db_profile.veriff_session_id = session_id
        db.session.add(VerificationAuditLog(user_id=user.user_id, action="veriff_session", details=session_id))
        db.session.commit()
    except Exception as exc:
        log(f"Veriff error for {user.user_id}: {exc}")


def submit_au_strac_smr(user: UserProfile, reason: str) -> None:
    from . import aml

    log(f"SMR submitted for {user.user_id}: {reason}")
    aml.report_user_suspicion(user.user_id, reason)


def store_kyc_information(user_id: int, info_type: str, info_data: str) -> None:
    """Persist KYC data with a 7 year retention period."""
    retention = datetime.utcnow() + timedelta(days=365 * 7)
    record = KYCRecord(
        user_id=user_id,
        info_type=info_type,
        info_data=info_data,
        retention_until=retention,
    )
    db.session.add(record)
    db.session.add(
        AMLLogEntry(
            user_id=user_id,
            action="kyc_recorded",
            details=info_type,
        )
    )
    db.session.commit()


def warn_user(user: UserProfile, message: str) -> None:
    log(f"Warning user {user.user_id}: {message}")


def log(message: str) -> None:
    logging.getLogger("kyc").info(message)
