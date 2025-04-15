"""edit models

Revision ID: a9a8de0ad170
Revises: b32fa197a060
Create Date: 2025-04-06 20:29:03.197089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9a8de0ad170'
down_revision: Union[str, None] = 'b32fa197a060'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('team_name', sa.String(), nullable=False))
    op.drop_column('users', 'team_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('users', 'team_name')
    # ### end Alembic commands ###
