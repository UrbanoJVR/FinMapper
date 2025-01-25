"""empty message

Revision ID: c32efc9b4e01
Revises: 567e4b3a5c08
Create Date: 2025-01-25 16:38:58.537729

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c32efc9b4e01'
down_revision = '567e4b3a5c08'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comments', sa.String(length=100), nullable=True))


def downgrade():
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_column('comments')
