"""make fines.violation_type_id not null

Revision ID: f8a5f3140318
Revises: e746bf9a7c8a
Create Date: 2026-11-17 00:00:44.841580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8a5f3140318'
down_revision: Union[str, Sequence[str], None] = 'e746bf9a7c8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        sa.text("""
            UPDATE fines
            SET violation_type_id = (
                SELECT id FROM violation_types WHERE code = 'legacy_fine'
            )
            WHERE violation_type_id IS NULL
        """)
    )

    op.alter_column('fines', 'violation_type_id',
               existing_type=sa.UUID(),
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('fines', 'violation_type_id',
               existing_type=sa.UUID(),
               nullable=True)
