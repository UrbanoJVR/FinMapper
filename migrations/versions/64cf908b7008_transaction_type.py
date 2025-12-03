"""empty message

Revision ID: 64cf908b7008
Revises: c32efc9b4e01
Create Date: 2025-12-02 00:31:18.500188

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '64cf908b7008'
down_revision = 'c32efc9b4e01'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.add_column(sa.Column(
            'type',
            sa.String(length=10),
            nullable=False,
            server_default='EXPENSE'
        ))

    op.execute("""
               UPDATE transactions
               SET amount = amount * -1
               """)

    with op.batch_alter_table('transactions') as batch_op:
        batch_op.alter_column('type', server_default=None)


def downgrade():
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_column('type')
