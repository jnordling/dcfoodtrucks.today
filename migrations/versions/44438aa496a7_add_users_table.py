"""add users table

Revision ID: 44438aa496a7
Revises: 5a52448403b0
Create Date: 2015-07-02 16:25:49.353719

"""

# revision identifiers, used by Alembic.
revision = '44438aa496a7'
down_revision = '5a52448403b0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tw_user_id', sa.String(length=64), nullable=True),
    sa.Column('tw_oauth_token', sa.String(length=256), nullable=True),
    sa.Column('tw_oauth_secret', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('avatar', sa.String(length=512), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'trucks', sa.Column('user_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'trucks', 'user_id')
    op.drop_table('users')
    ### end Alembic commands ###
