"""initial: users

Revision ID: 0001
Revises:
"""
import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("username", sa.String(64), server_default=""),
        sa.Column("level", sa.String(16), server_default="A1"),
        sa.Column("streak", sa.Integer(), server_default="0"),
        sa.Column("last_lesson", sa.String(16), server_default=""),
        sa.Column("placement_done", sa.Boolean(), server_default=sa.false()),
        sa.Column("lesson_hour", sa.Integer(), server_default="8"),
        sa.Column("readiness", sa.JSON(), nullable=True),
        sa.Column("exam_date", sa.String(16), server_default=""),
        sa.Column("exam_date_confirmed", sa.Boolean(), server_default=sa.false()),
        sa.Column("access_status", sa.String(16), server_default="pending"),
        sa.Column("access_until", sa.String(16), server_default=""),
        sa.Column("requested_at", sa.String(32), server_default=""),
        sa.Column("decided_at", sa.String(32), server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("users")
