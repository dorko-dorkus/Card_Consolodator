"""add token column and remove card_number"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('gift_cards', sa.Column('token', sa.String(), nullable=True))
    op.drop_column('gift_cards', 'card_number')
    op.alter_column('gift_cards', 'token', nullable=False)
    op.create_unique_constraint('uq_gift_cards_token', 'gift_cards', ['token'])


def downgrade():
    op.add_column('gift_cards', sa.Column('card_number', sa.String(), nullable=True))
    op.drop_constraint('uq_gift_cards_token', 'gift_cards', type_='unique')
    op.drop_column('gift_cards', 'token')
    op.alter_column('gift_cards', 'card_number', nullable=False)
    op.create_unique_constraint('uq_gift_cards_card_number', 'gift_cards', ['card_number'])
