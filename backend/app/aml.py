import logging
import os
from datetime import datetime, timedelta

from .kyc import get_user_profile, process_transaction

from .models import (
    db,
    Transaction,
    SuspiciousMatterReportEntry,
    AMLLogEntry,
)

AUSTRAC_API_URL = os.getenv("AUSTRAC_API_URL", "https://api.austrac.gov.au/smr/submit")
APP_ENTITY_ID = os.getenv("APP_ENTITY_ID", "APP_ENTITY")
ENABLE_LIVE_SUBMISSION = os.getenv("ENABLE_LIVE_SUBMISSION", "false").lower() == "true"
LOCAL_SM_LOG_PATH = os.getenv("LOCAL_SM_LOG_PATH", "suspicious_reports.log")

SMR_DEADLINE_HOURS = int(os.getenv("SMR_DEADLINE_HOURS", "72"))

AML_THRESHOLD = float(os.getenv("AML_THRESHOLD", "10000"))


def build_suspicious_matter_report(txn: Transaction, reason: str) -> dict:
    """Create the payload for a Suspicious Matter Report."""
    return {
        "reporting_entity_id": APP_ENTITY_ID,
        "suspicious_transaction_id": txn.transaction_id,
        "user_id": txn.user_id,
        "timestamp": txn.timestamp.isoformat(),
        "amount": txn.amount,
        "transaction_type": txn.transaction_type,
        "reason": reason,
    }


def manual_review(report: dict) -> None:
    """Persist the report for manual compliance review."""
    with open(LOCAL_SM_LOG_PATH, "a") as fh:
        import json

        json.dump(report, fh)
        fh.write("\n")


def submit_suspicious_matter_report(report: dict) -> str:
    """Submit the report to AUSTRAC or queue for manual review."""
    if ENABLE_LIVE_SUBMISSION:
        import requests

        resp = requests.post(AUSTRAC_API_URL, json=report, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError("AUSTRAC SMR submission failed")
        return "Submitted"
    else:
        manual_review(report)
        return "Pending manual review"


def log_transaction(user_id: int, amount: float, transaction_type: str, stripe_payment_id: str | None = None) -> Transaction:
    """Persist the transaction and trigger monitoring checks."""
    txn = Transaction(
        user_id=user_id,
        amount=amount,
        transaction_type=transaction_type,
        stripe_payment_id=stripe_payment_id,
        timestamp=datetime.utcnow(),
    )
    db.session.add(txn)
    db.session.commit()

    # persist AML log entry
    db.session.add(
        AMLLogEntry(
            user_id=user_id,
            action="transaction_logged",
            details=f"{transaction_type}:{amount}",
            timestamp=txn.timestamp,
        )
    )
    db.session.commit()

    # Update KYC/AML monitoring profile
    try:
        profile = get_user_profile(user_id)
        process_transaction(profile, amount, transaction_type, [])
    except Exception as exc:
        logging.getLogger("aml").error("KYC processing failed: %s", exc)

    if amount >= AML_THRESHOLD:
        report_suspicious_activity(txn, reason="Amount exceeds threshold")
    return txn


def report_suspicious_activity(txn: Transaction, reason: str) -> None:
    """Log a suspicious matter report entry.

    In production this would submit an SMR to AUSTRAC. Here we simply log a
    warning for compliance review.
    """
    logger = logging.getLogger("aml")
    logger.warning(
        "Suspicious transaction detected",
        extra={
            "transaction_id": txn.transaction_id,
            "user_id": txn.user_id,
            "amount": txn.amount,
            "timestamp": txn.timestamp.isoformat(),
            "reason": reason,
        },
    )

    try:
        report = build_suspicious_matter_report(txn, reason)
        required_by = txn.timestamp + timedelta(hours=SMR_DEADLINE_HOURS)
        if datetime.utcnow() > required_by:
            raise RuntimeError("SMR submission overdue")
        result = submit_suspicious_matter_report(report)
        db.session.add(
            SuspiciousMatterReportEntry(
                user_id=txn.user_id,
                transaction_id=txn.transaction_id,
                report_json=str(report),
                reason=reason,
                required_by=required_by,
                submitted_at=datetime.utcnow() if ENABLE_LIVE_SUBMISSION else None,
            )
        )
        db.session.add(
            AMLLogEntry(
                user_id=txn.user_id,
                action="smr_submitted" if ENABLE_LIVE_SUBMISSION else "smr_queued",
                details=str(report),
            )
        )
        db.session.commit()
        logger.info("SMR processed: %s", result)
    except Exception as exc:
        logger.error("SMR handling failed: %s", exc)


def report_user_suspicion(user_id: int, reason: str) -> None:
    """Log a suspicious matter report not tied to a transaction."""
    logger = logging.getLogger("aml")
    now = datetime.utcnow()
    report = {
        "reporting_entity_id": APP_ENTITY_ID,
        "user_id": user_id,
        "timestamp": now.isoformat(),
        "reason": reason,
    }
    required_by = now + timedelta(hours=SMR_DEADLINE_HOURS)
    try:
        if datetime.utcnow() > required_by:
            raise RuntimeError("SMR submission overdue")
        result = submit_suspicious_matter_report(report)
        db.session.add(
            SuspiciousMatterReportEntry(
                user_id=user_id,
                transaction_id=None,
                report_json=str(report),
                reason=reason,
                required_by=required_by,
                submitted_at=datetime.utcnow() if ENABLE_LIVE_SUBMISSION else None,
            )
        )
        db.session.add(
            AMLLogEntry(
                user_id=user_id,
                action="smr_submitted" if ENABLE_LIVE_SUBMISSION else "smr_queued",
                details=str(report),
            )
        )
        db.session.commit()
        logger.info("SMR processed: %s", result)
    except Exception as exc:
        logger.error("SMR handling failed: %s", exc)
