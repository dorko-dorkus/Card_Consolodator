import argparse
import csv
import os
from datetime import datetime

from . import create_app, db
from .models import KYCRecord, SuspiciousMatterReportEntry, AMLLogEntry


def export_table(session, model, path):
    """Export a single SQLAlchemy model to CSV."""
    records = session.query(model).all()
    if not records:
        return 0
    columns = [c.name for c in model.__table__.columns]
    with open(path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(columns)
        for rec in records:
            writer.writerow([getattr(rec, c) for c in columns])
    return len(records)


def main(out_dir: str):
    app = create_app()
    with app.app_context():
        os.makedirs(out_dir, exist_ok=True)
        session = db.session
        counts = {}
        counts['kyc'] = export_table(session, KYCRecord, os.path.join(out_dir, 'kyc_records.csv'))
        counts['smr'] = export_table(session, SuspiciousMatterReportEntry, os.path.join(out_dir, 'suspicious_matter_reports.csv'))
        counts['aml'] = export_table(session, AMLLogEntry, os.path.join(out_dir, 'aml_logs.csv'))
        print("Exported records:", counts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export compliance records to CSV files')
    parser.add_argument('--out-dir', default='exports', help='Directory to write CSV files')
    args = parser.parse_args()
    main(args.out_dir)
