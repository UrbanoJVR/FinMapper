"""enable foreign keys

Revision ID: 527290ae3412
Revises: 
Create Date: 2024-05-09 22:39:03.617644

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '527290ae3412'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("PRAGMA foreign_keys = ON")


def downgrade():
    op.execute("PRAGMA foreign_keys = OFF")
