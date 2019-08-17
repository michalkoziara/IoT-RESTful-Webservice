"""empty message

Revision ID: 0e2c13f2d9ac
Revises: 3da46414f696
Create Date: 2019-08-16 20:27:23.046269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e2c13f2d9ac'
down_revision = '3da46414f696'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
