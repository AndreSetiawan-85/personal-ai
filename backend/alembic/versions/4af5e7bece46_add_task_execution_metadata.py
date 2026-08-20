"""add task execution metadata

Revision ID: 4af5e7bece46
Revises: ed50dd3a9a9c
Create Date: 2026-08-20
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "4af5e7bece46"
down_revision: Union[str, Sequence[str], None] = "ed50dd3a9a9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "run_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "tasks",
        sa.Column(
            "error_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "tasks",
        sa.Column(
            "last_error",
            sa.Text(),
            nullable=True,
        ),
    )

    # Setelah data lama sudah punya nilai 0,
    # default database tidak perlu dipertahankan.
    op.alter_column(
        "tasks",
        "run_count",
        server_default=None,
    )

    op.alter_column(
        "tasks",
        "error_count",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("tasks", "last_error")
    op.drop_column("tasks", "error_count")
    op.drop_column("tasks", "run_count")