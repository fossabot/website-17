"""

Revision ID: 7f447c94347a
Revises: a78f4b5d7dee
Create Date: 2017-11-17 14:59:36.177805
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f447c94347a'
down_revision = 'a78f4b5d7dee'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('uploads_count', sa.SmallInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'uploads_count')
    # ### end Alembic commands ###
