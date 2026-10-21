"""Adding pg vector supoort

Revision ID: f754f1dad8d3
Revises: 3e9d48d6780b
Create Date: 2026-10-20 14:06:14.815462

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f754f1dad8d3"
down_revision: str | Sequence[str] | None = "3e9d48d6780b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector")
