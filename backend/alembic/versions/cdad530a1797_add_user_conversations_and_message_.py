"""add user conversations and message relationships

Revision ID: cdad530a1797
Revises: ab1a31523017
Create Date: 2026-08-18 14:48:11.525845
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "cdad530a1797"
down_revision: Union[str, Sequence[str], None] = "ab1a31523017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("messages", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "user_id",
                sa.Integer(),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "conversation_id",
                sa.Integer(),
                nullable=True,
            )
        )
        batch_op.create_index(
            "ix_messages_user_id",
            ["user_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_messages_conversation_id",
            ["conversation_id"],
            unique=False,
        )
        batch_op.create_foreign_key(
            "fk_messages_conversation_id",
            "conversations",
            ["conversation_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    with op.batch_alter_table("messages", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_messages_conversation_id",
            type_="foreignkey",
        )
        batch_op.drop_index("ix_messages_conversation_id")
        batch_op.drop_index("ix_messages_user_id")
        batch_op.drop_column("conversation_id")
        batch_op.drop_column("user_id")