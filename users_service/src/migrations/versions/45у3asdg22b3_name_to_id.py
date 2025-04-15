"""name_to_id

Revision ID: c21f9870dabc
Revises: 39e3ad6628b8
Create Date: 2025-04-15 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c21f9870dabc'
down_revision: Union[str, None] = '39e3ad6628b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("team_name")
        batch_op.add_column(sa.Column("team_id", sa.Integer(), nullable=False))
        batch_op.drop_column("department_name")
        batch_op.add_column(sa.Column("department_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("team_id")
        batch_op.add_column(sa.Column("team_name", sa.String(), nullable=False))
        batch_op.drop_column("department_id")
        batch_op.add_column(sa.Column("department_name", sa.String(), nullable=True))