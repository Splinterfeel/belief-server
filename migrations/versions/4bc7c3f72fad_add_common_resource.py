"""add common.resource

Revision ID: 4bc7c3f72fad
Revises: 5b6907a9e33b
Create Date: 2024-05-03 22:45:16.014145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bc7c3f72fad'
down_revision: Union[str, None] = '5b6907a9e33b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resource',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('gold', sa.BigInteger(), server_default='100', nullable=False),
    sa.Column('materials', sa.BigInteger(), server_default='1000', nullable=False),
    sa.Column('food', sa.BigInteger(), server_default='1000', nullable=False),
    sa.Column('population', sa.BigInteger(), server_default='1000', nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['common.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id'),
    schema='common'
    )
    op.drop_column('user', 'money', schema='common')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('money', sa.BIGINT(), server_default=sa.text("'100'::bigint"), autoincrement=False, nullable=False), schema='common')
    op.drop_table('resource', schema='common')
    # ### end Alembic commands ###