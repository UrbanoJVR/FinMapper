"""Category name unique

Revision ID: 567e4b3a5c08
Revises: 7525395bd777
Create Date: 2024-05-14 23:37:32.327402

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '567e4b3a5c08'
down_revision = '7525395bd777'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.create_unique_constraint('CategoryNameUnique', ['name'])


def downgrade():
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_constraint('CategoryNameUnique', type_='unique')
