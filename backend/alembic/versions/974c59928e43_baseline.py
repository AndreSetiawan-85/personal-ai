"""baseline

Revision ID: 974c59928e43
Revises: 
Create Date: 2026-08-18 14:46:10.045713
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '974c59928e43'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass