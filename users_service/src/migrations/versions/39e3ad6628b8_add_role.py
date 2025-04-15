"""add role

Revision ID: 39e3ad6628b8
Revises: a9a8de0ad170
Create Date: 2025-04-08 19:32:46.827835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39e3ad6628b8'
down_revision: Union[str, None] = 'a9a8de0ad170'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('role', sa.String(), nullable=False, server_default="employee"))
    op.add_column('users', sa.Column('department_name', sa.String(), nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'department_name')
    op.drop_column('users', 'role')

