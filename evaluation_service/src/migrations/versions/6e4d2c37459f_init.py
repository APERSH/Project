"""init

Revision ID: 6e4d2c37459f
Revises: 
Create Date: 2025-04-09 16:24:18.523812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e4d2c37459f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table('taskevaluations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('evaluator_id', sa.Integer(), nullable=False),
    sa.Column('executor_id', sa.Integer(), nullable=False),
    sa.Column('timeliness', sa.Integer(), nullable=False),
    sa.Column('quality', sa.Integer(), nullable=False),
    sa.Column('completeness', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('taskevaluations')

