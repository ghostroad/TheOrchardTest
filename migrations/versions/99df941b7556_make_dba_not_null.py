"""make dba not null

Revision ID: 99df941b7556
Revises: d904d747cd54
Create Date: 2019-04-09 12:16:30.977087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99df941b7556'
down_revision = 'd904d747cd54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('establishment', 'dba',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('establishment', 'dba',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
