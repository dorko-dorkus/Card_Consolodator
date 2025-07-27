"""initial database schema"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default=sa.text('false')),
        sa.Column('stripe_customer_id', sa.String(), nullable=True, unique=True),
    )
    op.create_table(
        'gift_cards',
        sa.Column('card_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('card_number', sa.String(), nullable=False, unique=True),
        sa.Column('balance', sa.Float(), nullable=False),
        sa.Column('expiry_date', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('source', sa.String(), nullable=False),
    )
    op.create_table(
        'platform_gift_cards',
        sa.Column('card_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('balance', sa.Float(), nullable=False),
        sa.Column('stripe_card_id', sa.String(), nullable=True, unique=True),
    )
    op.create_table(
        'transactions',
        sa.Column('transaction_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('transaction_type', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('details_encrypted', sa.String(), nullable=False),
        sa.Column('stripe_payment_id', sa.String(), nullable=True, unique=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table('transactions')
    op.drop_table('platform_gift_cards')
    op.drop_table('gift_cards')
    op.drop_table('users')
