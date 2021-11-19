"""add foreign-key to posts table

Revision ID: 17c24c07440f
Revises: 03e274abfb8d
Create Date: 2021-11-19 13:49:31.506782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17c24c07440f'
down_revision = '03e274abfb8d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(constraint_name='posts_users_fk', source_table='posts', local_cols=[
                          'owner_id'], referent_table='users', remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint(table_name='posts', constraint_name='posts_users_fk')
    op.drop_column('posts', 'owner_id')
