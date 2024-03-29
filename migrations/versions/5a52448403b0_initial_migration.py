"""initial migration

Revision ID: 5a52448403b0
Revises: None
Create Date: 2015-06-19 23:53:15.904011

"""

# revision identifiers, used by Alembic.
revision = '5a52448403b0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trucks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('display_name', sa.String(length=256), nullable=True),
    sa.Column('tw_handle', sa.String(length=128), nullable=True),
    sa.Column('website', sa.String(length=256), nullable=True),
    sa.Column('img_thumb', sa.String(length=512), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('last_tweet_id', sa.String(length=32), nullable=True),
    sa.Column('last_tweet_time', sa.DateTime(), nullable=True),
    sa.Column('last_tweet_text', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trucks')
    ### end Alembic commands ###
