"""add task retry policy

Revision ID: 7da6c4e806d4
Revises: 552021575263
Create Date: 2026-08-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7da6c4e806d4"
down_revision: Union[str, Sequence[str], None] = "552021575263"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "max_retries",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "tasks",
        sa.Column(
            "retry_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "tasks",
        sa.Column(
            "retry_delay",
            sa.Integer(),
            nullable=False,
            server_default="60",
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "tasks",
        "retry_delay",
    )

    op.drop_column(
        "tasks",
        "retry_count",
    )

    op.drop_column(
        "tasks",
        "max_retries",
    )