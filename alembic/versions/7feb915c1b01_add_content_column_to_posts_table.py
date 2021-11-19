"""add content column to posts table

Revision ID: 7feb915c1b01
Revises: add40ec1503f
Create Date: 2021-11-19 13:40:49.804609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7feb915c1b01'
down_revision = 'add40ec1503f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
