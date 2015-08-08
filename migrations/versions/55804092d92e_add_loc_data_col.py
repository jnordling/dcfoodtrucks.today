"""add loc data col

Revision ID: 55804092d92e
Revises: 2bce9768cc66
Create Date: 2015-08-01 13:52:23.825530

"""

# revision identifiers, used by Alembic.
revision = '55804092d92e'
down_revision = '2bce9768cc66'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trucks', sa.Column('loc_data', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trucks', 'loc_data')
    ### end Alembic commands ###