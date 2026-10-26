"""Added the collection name for the vectorstore

Revision ID: ca6f13f21955
Revises: bf05d00743a6
Create Date: 2026-10-20 11:44:46.107128

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from backend.core.settings import get_settings

# revision identifiers, used by Alembic.
revision: str = "ca6f13f21955"
down_revision: str | Sequence[str] | None = "bf05d00743a6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    columns = inspector.get_columns("course_vector_store")

    if any(column["name"] == "collection_name" for column in columns):
        return

    collection_name = get_settings().ASTRA_DB_COLLECTION_NAME
    op.add_column(
        "course_vector_store",
        sa.Column("collection_name", sa.String(), nullable=True),
    )
    records = sa.table("course_vector_store", sa.column("collection_name", sa.String()))
    op.execute(records.update().values(collection_name=collection_name))
    with op.batch_alter_table("course_vector_store") as batch_op:
        batch_op.alter_column(
            "collection_name", existing_type=sa.String(), nullable=False
        )


def downgrade() -> None:
    with op.batch_alter_table("course_vector_store") as batch_op:
        batch_op.drop_column("collection_name")
