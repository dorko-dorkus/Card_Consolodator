"""add verification tables"""
from alembic import op
import sqlalchemy as sa

revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_profiles',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id'), primary_key=True),
        sa.Column('verification_status', sa.String(), nullable=False, server_default='not_verified'),
        sa.Column('veriff_session_id', sa.String(), nullable=True),
        sa.Column('flagged', sa.Boolean(), nullable=True, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )
    op.create_table(
        'identification_documents',
        sa.Column('doc_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user_profiles.user_id'), nullable=False),
        sa.Column('doc_type', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )
    op.create_table(
        'verification_audit_logs',
        sa.Column('log_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user_profiles.user_id'), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('details', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('verification_audit_logs')
    op.drop_table('identification_documents')
    op.drop_table('user_profiles')
