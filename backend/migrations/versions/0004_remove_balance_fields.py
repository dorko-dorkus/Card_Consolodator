"""remove balance columns from gift cards"""
from alembic import op
import sqlalchemy as sa

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('gift_cards') as batch:
        batch.drop_column('balance')
    with op.batch_alter_table('platform_gift_cards') as batch:
        batch.drop_column('balance')


def downgrade():
    with op.batch_alter_table('gift_cards') as batch:
        batch.add_column(sa.Column('balance', sa.Float(), nullable=False))
    with op.batch_alter_table('platform_gift_cards') as batch:
        batch.add_column(sa.Column('balance', sa.Float(), nullable=False))
