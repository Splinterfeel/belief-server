"""drop queue uq

Revision ID: 9eb6d25f156c
Revises: 80201da037f6
Create Date: 2024-05-11 20:21:49.034927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9eb6d25f156c'
down_revision: Union[str, None] = '80201da037f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_buildingqueue_stronghold_cell', 'building', schema='queued', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_buildingqueue_stronghold_cell', 'building', ['stronghold_id', 'cell', 'done'], schema='queued')
    # ### end Alembic commands ###
