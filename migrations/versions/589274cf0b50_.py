# pylint: skip-file
"""empty message

Revision ID: 589274cf0b50
Revises: bc5bdfa8b2fa
Create Date: 2019-11-08 21:49:48.276612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '589274cf0b50'
down_revision = 'bc5bdfa8b2fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('executive_device', 'state')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('executive_device', sa.Column('state', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    # ### end Alembic commands ###