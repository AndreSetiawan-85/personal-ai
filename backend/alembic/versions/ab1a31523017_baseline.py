"""baseline

Revision ID: ab1a31523017
Revises: 974c59928e43
Create Date: 2026-08-18 14:46:33.391978
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ab1a31523017'
down_revision: Union[str, Sequence[str], None] = '974c59928e43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass