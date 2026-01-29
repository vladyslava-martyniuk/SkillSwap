from sqlalchemy import Table, Column, Integer, ForeignKey
from base import Base

# ---------- MATCHES ----------
# Зв'язок "багато до багатьох" між навичками і користувачами
# Наприклад, студент (student_id) хоче вчитися навичці (skill_id)
matches = Table(
    "matches",
    Base.metadata,
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
    Column("student_id", Integer, ForeignKey("users.id"), primary_key=True),
)
