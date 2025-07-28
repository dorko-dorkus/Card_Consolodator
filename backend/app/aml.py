import logging
import os
from datetime import datetime

from .models import db, Transaction

AUSTRAC_API_URL = os.getenv("AUSTRAC_API_URL", "https://api.austrac.gov.au/smr/submit")
APP_ENTITY_ID = os.getenv("APP_ENTITY_ID", "APP_ENTITY")
ENABLE_LIVE_SUBMISSION = os.getenv("ENABLE_LIVE_SUBMISSION", "false").lower() == "true"
LOCAL_SM_LOG_PATH = os.getenv("LOCAL_SM_LOG_PATH", "suspicious_reports.log")

AML_THRESHOLD = float(os.getenv("AML_THRESHOLD", "10000"))


def build_suspicious_matter_report(txn: Transaction) -> dict:
    """Create the payload for a Suspicious Matter Report."""
    return {
        "reporting_entity_id": APP_ENTITY_ID,
        "suspicious_transaction_id": txn.transaction_id,
        "user_id": txn.user_id,
        "timestamp": txn.timestamp.isoformat(),
        "amount": txn.amount,
        "transaction_type": txn.transaction_type,
    }


def submit_suspicious_matter_report(report: dict) -> str:
    """Submit the report to AUSTRAC or save it locally."""
    if ENABLE_LIVE_SUBMISSION:
        import requests

        resp = requests.post(AUSTRAC_API_URL, json=report, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError("AUSTRAC SMR submission failed")
        return "Submitted"
    else:
        with open(LOCAL_SM_LOG_PATH, "a") as fh:
            import json

            json.dump(report, fh)
            fh.write("\n")
        return "Saved locally for compliance review"


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

    if amount >= AML_THRESHOLD:
        report_suspicious_activity(txn)
    return txn


def report_suspicious_activity(txn: Transaction) -> None:
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
        },
    )

    try:
        report = build_suspicious_matter_report(txn)
        result = submit_suspicious_matter_report(report)
        logger.info("SMR processed: %s", result)
    except Exception as exc:
        logger.error("SMR handling failed: %s", exc)
