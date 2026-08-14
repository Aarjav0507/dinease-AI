"""add reservation fee waived and food total amount

Revision ID: 39792c5541ff
Revises: ecbdad83d9b5
Create Date: 2026-08-12 16:20:51.686291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39792c5541ff'
down_revision: Union[str, Sequence[str], None] = 'ecbdad83d9b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        'orders',
        sa.Column(
            'food_total_amount',
            sa.Numeric(10, 2),
            nullable=False,
            server_default='0'
        )
    )

    op.add_column(
        'reservations',
        sa.Column(
            'reservation_fee_waived',
            sa.Boolean(),
            nullable=False,
            server_default='0'
        )
    )