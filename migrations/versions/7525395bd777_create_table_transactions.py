"""create table transactions

Revision ID: 7525395bd777
Revises: 78141cfc5835
Create Date: 2024-05-09 22:46:34.268746

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7525395bd777'
down_revision = '78141cfc5835'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('transactions',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('date', sa.Date(), nullable=False),
                    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
                    sa.Column('concept', sa.String(length=100), nullable=False),
                    sa.Column('category_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='RESTRICT'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('transactions')
