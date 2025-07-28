import logging
import os
from datetime import datetime

from .models import db, Transaction

AML_THRESHOLD = float(os.getenv("AML_THRESHOLD", "10000"))


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
