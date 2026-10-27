"""Added created at and updated at for processing run

Revision ID: 3fb8865b66fd
Revises: 17905e6b3b17
Create Date: 2026-10-22 16:50:37.978840

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3fb8865b66fd"
down_revision: str | Sequence[str] | None = "17905e6b3b17"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add timestamps and backfill existing processing runs."""
    with op.batch_alter_table("processing_run") as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            )
        )
        batch_op.add_column(
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            )
        )

    with op.batch_alter_table("processing_run") as batch_op:
        batch_op.alter_column("created_at", server_default=None)
        batch_op.alter_column("updated_at", server_default=None)


def downgrade() -> None:
    """Remove processing run timestamps."""
    with op.batch_alter_table("processing_run") as batch_op:
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")
