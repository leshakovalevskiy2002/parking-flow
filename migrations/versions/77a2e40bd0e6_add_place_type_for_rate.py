"""add place_type for Rate

Revision ID: 77a2e40bd0e6
Revises: d643a4e0c8f3
Create Date: 2026-10-18 00:08:02.584922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77a2e40bd0e6'
down_revision: Union[str, Sequence[str], None] = 'd643a4e0c8f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('rates', sa.Column('place_type', sa.Enum('REGULAR', 'DISABLED', 'VIP', name='parking_type_enum'), server_default='REGULAR', nullable=False))


def downgrade() -> None:
    op.drop_column('rates', 'place_type')
