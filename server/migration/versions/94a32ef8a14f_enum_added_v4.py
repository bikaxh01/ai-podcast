"""enum added v4

Revision ID: 94a32ef8a14f
Revises: 87bee0d69b16
Create Date: 2025-07-17 21:52:21.457514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
# revision identifiers, used by Alembic.
revision: str = '94a32ef8a14f'
down_revision: Union[str, Sequence[str], None] = '87bee0d69b16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new value to enum
    op.execute("ALTER TYPE podcast_status ADD VALUE IF NOT EXISTS 'NEW_ADDED';")

def downgrade() -> None:
    # Downgrade for enums is tricky; you can't remove values directly.
    # You may want to leave this as pass, or document that manual intervention is needed.
    pass