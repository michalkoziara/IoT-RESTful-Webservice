# pylint: skip-file
"""empty message

Revision ID: 087dd125ce10
Revises: a26657686ab1
Create Date: 2019-10-18 18:45:41.943906

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '087dd125ce10'
down_revision = 'a26657686ab1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('username', sa.String(length=255), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('registered_on', sa.DateTime(), nullable=False),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    op.add_column('device_group', sa.Column('admin_id', sa.Integer(), nullable=True))
    op.drop_constraint('device_group_user_id_fkey', 'device_group', type_='foreignkey')
    op.create_foreign_key(None, 'device_group', 'admin', ['admin_id'], ['id'])
    op.drop_column('device_group', 'user_id')
    op.drop_column('user', 'is_admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('device_group', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'device_group', type_='foreignkey')
    op.create_foreign_key('device_group_user_id_fkey', 'device_group', 'user', ['user_id'], ['id'])
    op.drop_column('device_group', 'admin_id')
    op.drop_table('admin')
    # ### end Alembic commands ###
