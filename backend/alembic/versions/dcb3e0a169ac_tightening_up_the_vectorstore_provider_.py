"""Tighten the vector-store provider column with an enum."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "dcb3e0a169ac"
down_revision = "0fdfeecf3db5"
branch_labels = None
depends_on = None

provider_enum = postgresql.ENUM(
    "ASTRA",
    "POSTGRES",
    name="vector_store_provider",
    create_type=False,
)


def upgrade() -> None:
    provider_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "course_vector_store",
        "provider",
        existing_type=sa.VARCHAR(),
        type_=provider_enum,
        existing_nullable=False,
        postgresql_using="upper(provider::text)::vector_store_provider",
    )


def downgrade() -> None:
    op.alter_column(
        "course_vector_store",
        "provider",
        existing_type=provider_enum,
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="lower(provider::text)",
    )

    provider_enum.drop(op.get_bind(), checkfirst=True)
