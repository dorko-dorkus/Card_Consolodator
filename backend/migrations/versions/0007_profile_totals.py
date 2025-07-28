"""add transaction total fields to user profile"""
from alembic import op
import sqlalchemy as sa

revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user_profiles', sa.Column('daily_total', sa.Float(), nullable=False, server_default='0'))
    op.add_column('user_profiles', sa.Column('weekly_total', sa.Float(), nullable=False, server_default='0'))
    op.add_column('user_profiles', sa.Column('day', sa.Date(), nullable=True))
    op.add_column('user_profiles', sa.Column('week_start', sa.Date(), nullable=True))


def downgrade():
    op.drop_column('user_profiles', 'week_start')
    op.drop_column('user_profiles', 'day')
    op.drop_column('user_profiles', 'weekly_total')
    op.drop_column('user_profiles', 'daily_total')
