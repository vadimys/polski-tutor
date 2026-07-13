"""assignments.module + assignments.target (авто-залік за модулем)

Revision ID: 0010
Revises: 0009
"""
import sqlalchemy as sa
from alembic import op

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "assignments",
        sa.Column("module", sa.String(length=16), nullable=False, server_default=""),
    )
    op.add_column(
        "assignments",
        sa.Column("target", sa.Integer(), nullable=False, server_default="1"),
    )


def downgrade() -> None:
    op.drop_column("assignments", "target")
    op.drop_column("assignments", "module")
