"""Fixed foreign key constraints

Revision ID: 0ea0f59cfbb5
Revises: 21f1e43f3881
Create Date: 2025-03-06 20:30:32.434214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ea0f59cfbb5'
down_revision: Union[str, None] = '21f1e43f3881'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('builds', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('builds_user_id_fkey', 'builds', type_='foreignkey')
    op.create_foreign_key(None, 'builds', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'builds', type_='foreignkey')
    op.create_foreign_key('builds_user_id_fkey', 'builds', 'users', ['user_id'], ['id'])
    op.alter_column('builds', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
