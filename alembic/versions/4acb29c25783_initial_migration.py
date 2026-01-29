"""initial migration

Revision ID: 4acb29c25783
Revises: 
Create Date: 2026-01-23 09:58:29.916057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4acb29c25783'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- таблиця користувачів ---
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(length=50), unique=True, nullable=False),
        sa.Column("email", sa.String(length=120), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(length=128), nullable=False),
    )

    # --- таблиця навичок ---
    op.create_table(
        "skill",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("level", sa.String(length=50), nullable=False),
        sa.Column("can_teach", sa.Boolean, nullable=False, default=False),
        sa.Column("want_learn", sa.Boolean, nullable=False, default=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False),
    )

    # --- таблиця зв'язку "багато до багатьох" між навичками і користувачами ---
    op.create_table(
        "match",
        sa.Column("skill_id", sa.Integer, sa.ForeignKey("skill.id"), primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("user.id"), primary_key=True),
    )