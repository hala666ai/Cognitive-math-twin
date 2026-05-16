from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.db_init import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    grade = Column(String, nullable=True)
    cognitive_profile = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
