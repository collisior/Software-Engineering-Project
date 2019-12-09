"""empty message

Revision ID: a700c5ae62c2
Revises: 177b02f8bc2c
Create Date: 2019-12-08 20:24:13.271723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a700c5ae62c2'
down_revision = '177b02f8bc2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('spotify_object', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'spotify_object')
    # ### end Alembic commands ###