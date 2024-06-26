"""constraints building type and building tables

Revision ID: 8d2f5b463f6e
Revises: 7522a68444bf
Create Date: 2024-05-03 23:26:40.598518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d2f5b463f6e'
down_revision: Union[str, None] = '7522a68444bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'building', ['id'], schema='stronghold')
    op.create_unique_constraint(None, 'building_type', ['id'], schema='stronghold')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'building_type', schema='stronghold', type_='unique')
    op.drop_constraint(None, 'building', schema='stronghold', type_='unique')
    # ### end Alembic commands ###
