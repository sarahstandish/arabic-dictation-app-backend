"""empty message

Revision ID: 71656ec08ca0
Revises: af0a0df9842d
Create Date: 2022-01-24 13:00:26.610396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71656ec08ca0'
down_revision = 'af0a0df9842d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('voweled_word', sa.String(length=50), nullable=True),
    sa.Column('unvoweled_word', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('words')
    # ### end Alembic commands ###
