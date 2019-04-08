"""ratings table

Revision ID: a9ddbc1d01f7
Revises: c13a1bfb1016
Create Date: 2019-04-08 17:48:16.710978

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a9ddbc1d01f7'
down_revision = 'c13a1bfb1016'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grade', postgresql.ENUM('A', 'B', 'C', name='grade'), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('camis', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['camis'], ['establishment.camis'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rating')
    # ### end Alembic commands ###
