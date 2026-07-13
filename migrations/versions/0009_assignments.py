"""assignments (завдання викладача з дедлайном) + assignment_done (виконання)

Revision ID: 0009
Revises: 0008
"""
import sqlalchemy as sa
from alembic import op

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "assignments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("teacher_id", sa.BigInteger(), index=True),
        sa.Column("group_id", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("deadline", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "assignment_done",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "assignment_id",
            sa.Integer(),
            sa.ForeignKey("assignments.id", ondelete="CASCADE"),
            index=True,
        ),
        sa.Column("user_id", sa.BigInteger(), index=True),
        sa.Column("done_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("assignment_done")
    op.drop_table("assignments")
