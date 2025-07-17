"""enum added v5

Revision ID: 2125925de75d
Revises: 94a32ef8a14f
Create Date: 2025-07-17 21:56:23.727130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
# revision identifiers, used by Alembic.
revision: str = '2125925de75d'
down_revision: Union[str, Sequence[str], None] = '94a32ef8a14f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rename the old enum type
    op.execute("ALTER TYPE podcast_status RENAME TO podcast_status_old;")
    # Create the new enum type without the removed value
    op.execute("CREATE TYPE podcast_status AS ENUM ('PENDING', 'PROCESSING', 'COMPLETED','FAILED');")
    # Alter the column to use the new enum type
    op.execute("ALTER TABLE podcast ALTER COLUMN status TYPE podcast_status USING status::text::podcast_status;")
    # Drop the old enum type
    op.execute("DROP TYPE podcast_status_old;")


def downgrade() -> None:
    """Downgrade schema."""
    # (Optional) Reverse the process if needed
    pass
