# pylint: skip-file

"""empty message

Revision ID: e3e33f1611c3
Revises: 50446fa84014
Create Date: 2019-10-26 18:52:05.312143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3e33f1611c3'
down_revision = '50446fa84014'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'executive_device', ['device_group_id', 'name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'executive_device', type_='unique')
    # ### end Alembic commands ###
