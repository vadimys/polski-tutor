"""sessions.user_id → FK users(id) ON DELETE CASCADE

Revision ID: 0003
Revises: 0002
"""
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Прибрати можливі сироти (сесії без користувача), інакше FK не створиться
    op.execute("DELETE FROM sessions WHERE user_id NOT IN (SELECT id FROM users)")
    op.create_foreign_key(
        "fk_sessions_user_id",
        "sessions",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_sessions_user_id", "sessions", type_="foreignkey")
