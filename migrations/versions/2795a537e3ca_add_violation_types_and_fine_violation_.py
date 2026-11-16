"""add violation_types and fine.violation_type_id

Revision ID: 2795a537e3ca
Revises: 77a2e40bd0e6
Create Date: 2026-11-16 23:27:58.465521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2795a537e3ca'
down_revision: Union[str, Sequence[str], None] = '77a2e40bd0e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('violation_types',
    sa.Column('code', sa.String(length=100), nullable=False),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('amount > 0', name='ck_positive_violation_amount'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.add_column('fines', sa.Column('violation_type_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(
        'fk_fines_violation_type_id_violation_types',
        'fines',
        'violation_types',
        ['violation_type_id'],
        ['id']
    )


def downgrade() -> None:
    op.drop_constraint('fk_fines_violation_type_id_violation_types', 'fines', type_='foreignkey')
    op.drop_column('fines', 'violation_type_id')
    op.drop_table('violation_types')
