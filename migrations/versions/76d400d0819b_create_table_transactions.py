"""create table transactions

Revision ID: 76d400d0819b
Revises: a3c0355e2a71
Create Date: 2024-04-26 20:48:58.871671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76d400d0819b'
down_revision = 'a3c0355e2a71'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('concept', sa.String(length=100), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('transactions')
