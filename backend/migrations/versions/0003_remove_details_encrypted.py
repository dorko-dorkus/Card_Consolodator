"""remove sensitive transaction details"""
from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('transactions', 'details_encrypted')


def downgrade():
    op.add_column('transactions', sa.Column('details_encrypted', sa.String(), nullable=False))
