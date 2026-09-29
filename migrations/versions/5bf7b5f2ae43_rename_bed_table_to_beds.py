"""rename bed table to beds

Revision ID: 5bf7b5f2ae43
Revises: f00d9398bb5e
Create Date: 2026-09-29 19:59:04.986709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bf7b5f2ae43'
down_revision: Union[str, Sequence[str], None] = 'f00d9398bb5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('bed', 'beds')


def downgrade() -> None:
    op.rename_table('beds', 'bed')

