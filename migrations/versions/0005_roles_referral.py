"""users.role + users.referred_by — ролі (student/teacher) і реферали (B2B2C)

Revision ID: 0005
Revises: 0004
"""
import sqlalchemy as sa
from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.String(length=16), nullable=False, server_default="student"),
    )
    op.add_column(
        "users",
        sa.Column("referred_by", sa.BigInteger(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("users", "referred_by")
    op.drop_column("users", "role")
