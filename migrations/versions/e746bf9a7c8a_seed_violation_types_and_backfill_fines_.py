"""seed violation_types and backfill fines.violation_type_id

Revision ID: e746bf9a7c8a
Revises: 2795a537e3ca
Create Date: 2026-11-16 23:43:16.552372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e746bf9a7c8a'
down_revision: Union[str, Sequence[str], None] = '2795a537e3ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SYSTEM_VIOLATION_CODES = ("no_parking_session", "no_disabled_permission", "legacy_fine")

SEED_VIOLATION_TYPES = [
    {
        "code": "no_parking_session",
        "reason": "No parking session",
        "amount": 25.00,
    },
    {
        "code": "no_disabled_permission",
        "reason": "No disabled permission",
        "amount": 19.99,
    },
    {
        "code": "legacy_fine",
        "reason": "Legacy fine (migrated)",
        "amount": 0.01,
    },
]


def upgrade() -> None:
    """Upgrade schema."""
    for item in SEED_VIOLATION_TYPES:
        op.execute(
            sa.text(
                """
                INSERT INTO violation_types (code, reason, amount)
                VALUES (:code, :reason, :amount)
                ON CONFLICT (code) DO NOTHING
                """
            ).bindparams(
                code=item["code"],
                reason=item["reason"],
                amount=item["amount"],
            )
        )

    op.execute(
        sa.text(
            """
            UPDATE fines
            SET violation_type_id = (
                SELECT id FROM violation_types WHERE code = 'legacy_fine'
            )
            WHERE violation_type_id IS NULL
            """
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            """
            UPDATE fines
            SET violation_type_id = NULL
            WHERE violation_type_id = (
                SELECT id FROM violation_types WHERE code = 'legacy_fine'
            )
            """
        )
    )

    for code in SYSTEM_VIOLATION_CODES:
        op.execute(
            sa.text("DELETE FROM violation_types WHERE code = :code").bindparams(code=code)
        )
