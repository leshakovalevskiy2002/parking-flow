"""baseline

Revision ID: d643a4e0c8f3
Revises:
Create Date: 2026-10-17 00:38:55.101133

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = 'd643a4e0c8f3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Baseline: schema already exists in the database.

    This revision is a no-op. It marks the starting point for Alembic
    and is applied via `alembic stamp head` on existing databases.
    """
    pass


def downgrade() -> None:
    pass
