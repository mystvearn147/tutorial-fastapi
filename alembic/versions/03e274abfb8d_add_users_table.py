"""add users table

Revision ID: 03e274abfb8d
Revises: 7feb915c1b01
Create Date: 2021-11-19 13:43:42.121647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03e274abfb8d'
down_revision = '7feb915c1b01'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('email', sa.String(), nullable=False, unique=True), sa.Column(
        'password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade():
    op.drop_table('users')
