"""Fixed Foreign Key in PriceHistory

Revision ID: 21f1e43f3881
Revises: e3766c90449b
Create Date: 2025-03-05 22:45:41.225984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21f1e43f3881'
down_revision: Union[str, None] = 'e3766c90449b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('price_history', sa.Column('component_id', sa.Integer(), nullable=False))
    op.drop_constraint('price_history_part_id_fkey', 'price_history', type_='foreignkey')
    op.create_foreign_key(None, 'price_history', 'components', ['component_id'], ['id'], ondelete='CASCADE')
    op.drop_column('price_history', 'part_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('price_history', sa.Column('part_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'price_history', type_='foreignkey')
    op.create_foreign_key('price_history_part_id_fkey', 'price_history', 'pc_parts', ['part_id'], ['id'])
    op.drop_column('price_history', 'component_id')
    # ### end Alembic commands ###
