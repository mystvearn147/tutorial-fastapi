"""create posts table

Revision ID: add40ec1503f
Revises: 
Create Date: 2021-11-19 13:23:23.459613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add40ec1503f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(table_name='posts', columns=[sa.Column('id', sa.Integer(
    ), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False)])


def downgrade():
    op.drop_table(table_name='posts')
