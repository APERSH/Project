"""replace user_email with user_id

Revision ID: abc123def456
Revises: 42e8d6b7a605
Create Date: 2025-04-15 14:50:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abc123def456'
down_revision = '42e8d6b7a605'
branch_labels = None
depends_on = None


def upgrade():
    # Удаляем старую колонку
    op.drop_column('calendars', 'user_email')

    # Добавляем новую колонку
    op.add_column('calendars', sa.Column('user_id', sa.Integer(), nullable=False))


def downgrade():
    # Возвращаем user_email обратно
    op.add_column('calendars', sa.Column('user_email', sa.String(), nullable=False))

    # Удаляем user_id
    op.drop_column('calendars', 'user_id')