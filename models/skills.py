# models/skills.py
from sqlalchemy import Column, Integer, String, Boolean
from base import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)  # <- обов'язково
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    level = Column(String, nullable=False)
    can_teach = Column(Boolean, default=False)
    want_learn = Column(Boolean, default=False)
    user_id = Column(Integer, nullable=False)
