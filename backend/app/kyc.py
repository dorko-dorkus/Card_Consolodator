import logging
from datetime import datetime, timedelta

MAX_DAILY_TXN_LIMIT = 1000  # AUD
MAX_SINGLE_TXN_LIMIT = 300  # AUD soft flag threshold
MAX_BALANCE_LIMIT = 750  # AUD soft warning before hard KYC at 1000


class UserProfile:
    """Simple in-memory profile tracking AML/KYC status."""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.kyc_status = "not_verified"  # can be "not_verified", "pending", "verified"
        self.daily_total = 0.0
        self.weekly_total = 0.0
        self.card_balances: list[tuple[int, float]] = []
        self.txn_log: list[tuple[float, str, list, datetime]] = []
        self.flagged = False
        self._day = datetime.utcnow().date()
        self._week_start = self._day - timedelta(days=self._day.weekday())


_profiles: dict[int, UserProfile] = {}


def get_user_profile(user_id: int) -> UserProfile:
    profile = _profiles.get(user_id)
    if not profile:
        profile = UserProfile(user_id)
        _profiles[user_id] = profile
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


def process_transaction(user: UserProfile, amount: float, merchant_id: str, source_cards: list):
    _reset_totals_if_needed(user)

    if amount > MAX_SINGLE_TXN_LIMIT:
        flag_suspicious(user, reason="Single transaction exceeds soft threshold")

    user.daily_total += amount
    user.weekly_total += amount
    user.txn_log.append((amount, merchant_id, source_cards, datetime.utcnow()))

    total_consolidated = sum(balance for _, balance in user.card_balances)
    if total_consolidated > MAX_BALANCE_LIMIT:
        warn_user(user, message="Balance approaching AML threshold")

    if total_consolidated >= MAX_DAILY_TXN_LIMIT or user.weekly_total >= MAX_DAILY_TXN_LIMIT:
        trigger_kyc(user, reason="Exceeded AML transaction threshold")

    if detect_structuring(user):
        flag_suspicious(user, reason="Suspected structuring to avoid AML triggers")


def trigger_kyc(user: UserProfile, reason: str):
    if user.kyc_status != "verified":
        user.kyc_status = "pending"
        send_kyc_request(user, reason)


def detect_structuring(user: UserProfile) -> bool:
    txns = user.txn_log[-5:]
    if len(txns) >= 5 and all(t[0] < MAX_SINGLE_TXN_LIMIT for t in txns) and sum(t[0] for t in txns) > MAX_DAILY_TXN_LIMIT:
        return True
    return False


def flag_suspicious(user: UserProfile, reason: str):
    user.flagged = True
    submit_au_strac_smr(user, reason)


# Stubbed integration hooks -----------------------------------------------

def send_kyc_request(user: UserProfile, reason: str) -> None:
    log(f"KYC request triggered for {user.user_id}: {reason}")


def submit_au_strac_smr(user: UserProfile, reason: str) -> None:
    log(f"SMR submitted for {user.user_id}: {reason}")


def warn_user(user: UserProfile, message: str) -> None:
    log(f"Warning user {user.user_id}: {message}")


def log(message: str) -> None:
    logging.getLogger("kyc").info(message)
