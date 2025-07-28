"""Background compliance tasks."""
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_STOPPED

from .models import db, UserProfile, Transaction, SuspiciousMatterReportEntry
from .aml import SMR_DEADLINE_HOURS
from . import kyc

scheduler = BackgroundScheduler()
_atexit_registered = False

COMPLIANCE_LOGGER = logging.getLogger("compliance")


def alert_compliance(message: str) -> None:
    """Send an alert message to the compliance log."""
    COMPLIANCE_LOGGER.warning(message)


def review_transaction_patterns() -> None:
    """Check recent transactions for structuring or unusual behaviour."""
    now = datetime.utcnow()
    day_ago = now - timedelta(days=1)

    profiles = UserProfile.query.all()
    for profile in profiles:
        txns = (
            Transaction.query
            .filter(Transaction.user_id == profile.user_id,
                    Transaction.timestamp >= day_ago)
            .all()
        )
        amounts = [t.amount for t in txns if t.amount < kyc.MAX_SINGLE_TXN_LIMIT]
        if len(amounts) >= 3 and sum(amounts) > kyc.MAX_DAILY_TXN_LIMIT:
            user = kyc.get_user_profile(profile.user_id)
            kyc.flag_suspicious(user, reason="Structured transactions detected")
            alert_compliance(f"User {profile.user_id} flagged for structuring")
        if len(txns) >= 10:
            user = kyc.get_user_profile(profile.user_id)
            kyc.flag_suspicious(user, reason="High transaction volume")
            alert_compliance(f"User {profile.user_id} high volume transactions")


def review_pending_kyc() -> None:
    """Alert if profiles remain pending for too long."""
    cutoff = datetime.utcnow() - timedelta(days=3)
    pending = UserProfile.query.filter(
        UserProfile.verification_status == "pending",
        UserProfile.updated_at < cutoff,
    ).all()
    for profile in pending:
        alert_compliance(f"KYC pending >3 days for user {profile.user_id}")


def alert_flagged_profiles() -> None:
    """Notify compliance about flagged profiles."""
    flagged = UserProfile.query.filter_by(flagged=True).all()
    for profile in flagged:
        alert_compliance(f"User {profile.user_id} flagged for review")


def check_overdue_smrs() -> None:
    """Ensure all SMRs are submitted before the deadline."""
    now = datetime.utcnow()
    overdue = SuspiciousMatterReportEntry.query.filter(
        SuspiciousMatterReportEntry.submitted_at.is_(None),
        SuspiciousMatterReportEntry.required_by < now,
    ).all()
    for entry in overdue:
        alert_compliance(
            f"SMR for user {entry.user_id} overdue by "
            f"{(now - entry.required_by).total_seconds() / 3600:.1f}h"
        )


def init_scheduler(app):
    """Start background scheduler with compliance jobs."""
    global _atexit_registered
    if scheduler.state == STATE_STOPPED:
        scheduler.add_job(review_transaction_patterns, "interval", days=1)
        scheduler.add_job(review_pending_kyc, "interval", hours=24)
        scheduler.add_job(alert_flagged_profiles, "interval", hours=24)
        scheduler.add_job(check_overdue_smrs, "interval", hours=1)
        scheduler.start()
        if app.config.get("SCHEDULER_SHUTDOWN_AT_EXIT", True) and not _atexit_registered:
            import atexit
            atexit.register(lambda: scheduler.shutdown(wait=False))
            _atexit_registered = True
