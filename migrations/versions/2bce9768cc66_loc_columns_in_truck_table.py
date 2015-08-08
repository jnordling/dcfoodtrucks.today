"""loc columns in truck table

Revision ID: 2bce9768cc66
Revises: 44438aa496a7
Create Date: 2015-07-22 10:26:02.747229

"""

# revision identifiers, used by Alembic.
revision = '2bce9768cc66'
down_revision = '44438aa496a7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trucks', sa.Column('loc_display_address', sa.String(length=256), nullable=True))
    op.add_column('trucks', sa.Column('loc_lat', sa.Numeric(), nullable=True))
    op.add_column('trucks', sa.Column('loc_lng', sa.Numeric(), nullable=True))
    op.add_column('trucks', sa.Column('loc_source', sa.String(length=64), nullable=True))
    op.add_column('trucks', sa.Column('loc_updated', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trucks', 'loc_updated')
    op.drop_column('trucks', 'loc_source')
    op.drop_column('trucks', 'loc_lng')
    op.drop_column('trucks', 'loc_lat')
    op.drop_column('trucks', 'loc_display_address')
    ### end Alembic commands ###
