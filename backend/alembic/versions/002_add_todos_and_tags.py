"""Add todos and tags tables.

Revision ID: 002
Revises: 001
Create Date: 2025-12-31
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create priority enum
    op.execute("CREATE TYPE priority_level AS ENUM ('high', 'medium', 'low')")

    # Create recurrence enum
    op.execute("CREATE TYPE recurrence_pattern AS ENUM ('none', 'daily', 'weekly', 'monthly')")

    # Create todos table
    op.create_table(
        "todos",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "priority",
            sa.Enum("high", "medium", "low", name="priority_level", create_type=False),
            nullable=False,
            server_default="medium",
        ),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reminder_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "recurrence",
            sa.Enum("none", "daily", "weekly", "monthly", name="recurrence_pattern", create_type=False),
            nullable=False,
            server_default="none",
        ),
        sa.Column("parent_id", sa.UUID(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_id"], ["todos.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_todos_user_id", "todos", ["user_id"])
    op.create_index("ix_todos_user_completed", "todos", ["user_id", "completed"])
    op.create_index("ix_todos_user_priority", "todos", ["user_id", "priority"])
    op.create_index("ix_todos_user_due_date", "todos", ["user_id", "due_date"])

    # Create tags table
    op.create_table(
        "tags",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", "name", name="uq_tags_user_name"),
    )
    op.create_index("ix_tags_user_id", "tags", ["user_id"])

    # Create todo_tags junction table
    op.create_table(
        "todo_tags",
        sa.Column("todo_id", sa.UUID(), nullable=False),
        sa.Column("tag_id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("todo_id", "tag_id"),
        sa.ForeignKeyConstraint(["todo_id"], ["todos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("todo_tags")
    op.drop_index("ix_tags_user_id", table_name="tags")
    op.drop_table("tags")
    op.drop_index("ix_todos_user_due_date", table_name="todos")
    op.drop_index("ix_todos_user_priority", table_name="todos")
    op.drop_index("ix_todos_user_completed", table_name="todos")
    op.drop_index("ix_todos_user_id", table_name="todos")
    op.drop_table("todos")
    op.execute("DROP TYPE recurrence_pattern")
    op.execute("DROP TYPE priority_level")
