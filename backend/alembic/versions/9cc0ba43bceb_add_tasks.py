"""add tasks

Revision ID: 9cc0ba43bceb
Revises: cdad530a1797
Create Date: 2026-08-18 20:55:58.104563
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "9cc0ba43bceb"
down_revision: Union[str, Sequence[str], None] = "cdad530a1797"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("arguments", sa.JSON(), nullable=False),
        sa.Column("schedule", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("last_run_at", sa.DateTime(), nullable=True),
        sa.Column("next_run_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_tasks_id",
        "tasks",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_tasks_user_id",
        "tasks",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_tasks_status",
        "tasks",
        ["status"],
        unique=False,
    )
    op.create_index(
        "ix_tasks_next_run_at",
        "tasks",
        ["next_run_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_tasks_next_run_at",
        table_name="tasks",
    )
    op.drop_index(
        "ix_tasks_status",
        table_name="tasks",
    )
    op.drop_index(
        "ix_tasks_user_id",
        table_name="tasks",
    )
    op.drop_index(
        "ix_tasks_id",
        table_name="tasks",
    )
    op.drop_table("tasks")