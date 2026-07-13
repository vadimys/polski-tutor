"""FK+CASCADE на нові таблиці · UNIQUE(assignment_id,user_id) · payments.teacher_id + UNIQUE(charge_id)

Revision ID: 0011
Revises: 0010

Self-healing: перед додаванням FK прибирає осиротілі рядки (щоб міграція не впала
на бойових даних). Партійний unique-індекс на charge_id — лише PG (не в ORM-моделі).
"""
import sqlalchemy as sa
from alembic import op

revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 0. прибрати осиротілі рядки (інакше FK не створиться)
    op.execute("DELETE FROM assignment_done WHERE user_id NOT IN (SELECT id FROM users)")
    op.execute("DELETE FROM assignment_done WHERE assignment_id NOT IN (SELECT id FROM assignments)")
    op.execute("DELETE FROM assignments WHERE teacher_id NOT IN (SELECT id FROM users)")
    op.execute("DELETE FROM groups WHERE teacher_id NOT IN (SELECT id FROM users)")
    # дедуп можливих дублів (assignment_id,user_id) перед UNIQUE — лишаємо найменший id
    op.execute(
        "DELETE FROM assignment_done a USING assignment_done b "
        "WHERE a.assignment_id = b.assignment_id AND a.user_id = b.user_id AND a.id > b.id"
    )

    # 1. UNIQUE на assignment_done
    op.create_unique_constraint("uq_assignment_done", "assignment_done", ["assignment_id", "user_id"])

    # 2. FK CASCADE
    op.create_foreign_key(
        "fk_assignment_done_user", "assignment_done", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "fk_assignments_teacher", "assignments", "users", ["teacher_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "fk_groups_teacher", "groups", "users", ["teacher_id"], ["id"], ondelete="CASCADE"
    )

    # 3. payments.teacher_id (+ backfill з поточного referred_by) + partial UNIQUE на charge_id
    op.add_column(
        "payments", sa.Column("teacher_id", sa.BigInteger(), nullable=False, server_default="0")
    )
    op.create_index("ix_payments_teacher_id", "payments", ["teacher_id"])
    op.execute(
        "UPDATE payments SET teacher_id = COALESCE("
        "(SELECT referred_by FROM users WHERE users.id = payments.user_id), 0)"
    )
    op.execute(
        "CREATE UNIQUE INDEX uq_payments_charge_id ON payments (charge_id) WHERE charge_id <> ''"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uq_payments_charge_id")
    op.drop_index("ix_payments_teacher_id", table_name="payments")
    op.drop_column("payments", "teacher_id")
    op.drop_constraint("fk_groups_teacher", "groups", type_="foreignkey")
    op.drop_constraint("fk_assignments_teacher", "assignments", type_="foreignkey")
    op.drop_constraint("fk_assignment_done_user", "assignment_done", type_="foreignkey")
    op.drop_constraint("uq_assignment_done", "assignment_done", type_="unique")
