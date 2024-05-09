"""add bool upgrade to queue.building

Revision ID: 2afacdd8fd60
Revises: 8091f90d6cc4
Create Date: 2024-05-09 19:48:55.168281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2afacdd8fd60'
down_revision: Union[str, None] = '8091f90d6cc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('building', sa.Column('upgrade', sa.Boolean(), server_default='false', nullable=False), schema='queued')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('building', 'upgrade', schema='queued')
    # ### end Alembic commands ###
