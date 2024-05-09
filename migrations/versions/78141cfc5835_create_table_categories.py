"""create table categories

Revision ID: 78141cfc5835
Revises: 527290ae3412
Create Date: 2024-05-09 22:43:19.789097

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '78141cfc5835'
down_revision = '527290ae3412'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('categories',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(length=24), nullable=False),
                    sa.Column('description', sa.String(length=128), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('categories')
