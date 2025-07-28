"""add card balance table"""
from alembic import op
import sqlalchemy as sa

revision = '0008'
down_revision = '0007'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'card_balances',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id'), primary_key=True),
        sa.Column('card_id', sa.Integer(), primary_key=True),
        sa.Column('balance', sa.Float(), nullable=False, server_default='0'),
    )


def downgrade():
    op.drop_table('card_balances')
