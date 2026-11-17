"""add is_active to violation_types, has_disabled_permission to users

Revision ID: 17dbac9c3eac
Revises: f8a5f3140318
Create Date: 2026-11-17 00:12:24.692270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17dbac9c3eac'
down_revision: Union[str, Sequence[str], None] = 'f8a5f3140318'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('has_disabled_permission', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('violation_types', sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('violation_types', 'is_active')
    op.drop_column('users', 'has_disabled_permission')
