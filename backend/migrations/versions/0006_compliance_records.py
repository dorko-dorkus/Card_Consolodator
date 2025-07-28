"""add kyc, smr and aml log tables"""
from alembic import op
import sqlalchemy as sa

revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'kyc_records',
        sa.Column('record_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('info_type', sa.String(), nullable=False),
        sa.Column('info_data', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
        sa.Column('retention_until', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'suspicious_matter_reports',
        sa.Column('smr_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('transaction_id', sa.Integer(), sa.ForeignKey('transactions.transaction_id'), nullable=True),
        sa.Column('report_json', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )
    op.create_table(
        'aml_logs',
        sa.Column('log_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id'), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('details', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('aml_logs')
    op.drop_table('suspicious_matter_reports')
    op.drop_table('kyc_records')
