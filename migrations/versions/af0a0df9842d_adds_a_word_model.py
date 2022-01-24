"""adds a word model

Revision ID: af0a0df9842d
Revises: 
Create Date: 2022-01-24 12:56:06.188482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af0a0df9842d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('word',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('voweled_word', sa.String(length=50), nullable=True),
    sa.Column('unvoweled_word', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('word')
    # ### end Alembic commands ###
