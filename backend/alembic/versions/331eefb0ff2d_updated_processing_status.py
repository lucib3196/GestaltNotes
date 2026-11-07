"""Convert processing statuses to Celery-compatible values.

Revision ID: 331eefb0ff2d
Revises: 47a63ff3517c
Create Date: 2026-11-04 16:28:27.653517

"""

from collections.abc import Sequence

from alembic_postgresql_enum import TableReference

from alembic import op

revision: str = "331eefb0ff2d"
down_revision: str | Sequence[str] | None = "47a63ff3517c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Convert existing rows before replacing the enum labels."""
    # Celery has no partial-success state. Keep incomplete runs retryable.
    # This loses the distinction between partial and failed runs.
    op.execute("""
        UPDATE processing_run
        SET status = 'FAILED'
        WHERE status = 'PARTIAL'
    """)

    op.sync_enum_values(
        enum_schema="public",
        enum_name="processing_status",
        new_values=[
            "PENDING",
            "RECEIVED",
            "STARTED",
            "RETRY",
            "FAILURE",
            "SUCCESS",
            "REVOKED",
            "PROGRESS",
        ],
        affected_columns=[
            TableReference(
                table_schema="public",
                table_name="processing_run",
                column_name="status",
            )
        ],
        enum_values_to_rename=[
            ("QUEUED", "PENDING"),
            ("RUNNING", "STARTED"),
            ("RETRYING", "RETRY"),
            ("FAILED", "FAILURE"),
            ("SUCCEEDED", "SUCCESS"),
        ],
    )


def downgrade() -> None:
    """Restore old labels, normalizing states without an old equivalent."""
    # Original PARTIAL, RECEIVED, and PROGRESS values cannot be recovered.
    op.execute("""
        UPDATE processing_run
        SET status = CASE
            WHEN status = 'RECEIVED' THEN 'PENDING'::processing_status
            WHEN status = 'PROGRESS' THEN 'STARTED'::processing_status
            ELSE status
        END
        WHERE status IN ('RECEIVED', 'PROGRESS')
    """)

    op.sync_enum_values(
        enum_schema="public",
        enum_name="processing_status",
        new_values=[
            "QUEUED",
            "RUNNING",
            "RETRYING",
            "SUCCEEDED",
            "FAILED",
            "PARTIAL",
            "REVOKED",
        ],
        affected_columns=[
            TableReference(
                table_schema="public",
                table_name="processing_run",
                column_name="status",
            )
        ],
        enum_values_to_rename=[
            ("PENDING", "QUEUED"),
            ("STARTED", "RUNNING"),
            ("RETRY", "RETRYING"),
            ("FAILURE", "FAILED"),
            ("SUCCESS", "SUCCEEDED"),
        ],
    )
