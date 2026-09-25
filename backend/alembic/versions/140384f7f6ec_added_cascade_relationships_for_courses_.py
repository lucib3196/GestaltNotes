"""Added cascade relationships for courses models

Revision ID: 140384f7f6ec
Revises: 905eeefcccae
Create Date: 2026-09-24 15:50:26.863705

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "140384f7f6ec"
down_revision: str | Sequence[str] | None = "905eeefcccae"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    with op.batch_alter_table("course", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_course_owner_id"))
        if (
            inspector.get_pk_constraint("course").get("name")
            == "fk_course_owner_id_user"
        ):
            batch_op.drop_constraint(
                batch_op.f("fk_course_owner_id_user"),
                type_="foreignkey",
            )
        batch_op.create_foreign_key(
            batch_op.f("fk_course_owner_id_user"),
            "user",
            ["owner_id"],
            ["id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("course_access_code", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_course_access_code_course_id"))
        batch_op.drop_constraint(
            batch_op.f("course_access_code_course_id_fkey"),
            type_="foreignkey",
        )
        batch_op.create_foreign_key(
            batch_op.f("course_access_code_course_id_fkey"),
            "course",
            ["course_id"],
            ["id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("course_enrollment", schema=None) as batch_op:

        if (
            inspector.get_pk_constraint("course_enrollment").get("name")
            == "uq_course_enrollment_student_id"
        ):
            batch_op.drop_constraint(
                batch_op.f("uq_course_enrollment_student_id"),
                type_="foreignkey",
            )
        batch_op.create_unique_constraint(
            batch_op.f("uq_course_enrollment_student_id"),
            ["student_id", "course_id"],
        )

    with op.batch_alter_table("lecture_note", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("lecturenote_course_id_fkey"),
            type_="foreignkey",
        )
        batch_op.create_foreign_key(
            batch_op.f("lecturenote_course_id_fkey"),
            "course",
            ["course_id"],
            ["id"],
            ondelete="CASCADE",
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    with op.batch_alter_table("lecture_note", schema=None) as batch_op:
        print("PK", inspector.get_pk_constraint("lecture_note"))
        if (
            inspector.get_pk_constraint("lecture_note").get("name", None)
            == "lecturenote_pkey"
        ):
            batch_op.drop_constraint(
                batch_op.f("lecturenote_pkey"),
                type_="foreignkey",
            )
        if (
            inspector.get_pk_constraint("lecture_note").get("name", None)
            == "lecturenote_course_id_fkey"
        ):
            batch_op.drop_constraint(
                batch_op.f("lecturenote_course_id_fkey"),
                type_="foreignkey",
            )
        batch_op.create_foreign_key(
            batch_op.f("lecturenote_course_id_fkey"),
            "course",
            ["course_id"],
            ["id"],
        )

    with op.batch_alter_table("course_enrollment", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("uq_course_enrollment_student_id"),
            type_="unique",
        )

    with op.batch_alter_table("course_access_code", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("course_access_code_course_id_fkey"),
            type_="foreignkey",
        )
        batch_op.create_foreign_key(
            batch_op.f("course_access_code_course_id_fkey"),
            "course",
            ["course_id"],
            ["id"],
        )
        batch_op.create_index(
            batch_op.f("ix_course_access_code_course_id"),
            ["course_id"],
            unique=False,
        )

    with op.batch_alter_table("course", schema=None) as batch_op:
        if (
            inspector.get_pk_constraint("course").get("name")
            == "fk_course_owner_id_user"
        ):
            batch_op.drop_constraint(
                batch_op.f("fk_course_owner_id_user"),
                type_="foreignkey",
            )
            batch_op.create_foreign_key(
                batch_op.f("fk_course_owner_id_user"),
                "user",
                ["owner_id"],
                ["id"],
            )
        batch_op.create_index(
            batch_op.f("ix_course_owner_id"),
            ["owner_id"],
            unique=False,
        )
