from sqlalchemy import Column, Integer, ForeignKey, Boolean, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.db_init import Base

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), index=True)

    steps = Column(JSON, default=[])  # خطوات الطالب أثناء الحل
    is_correct = Column(Boolean, default=False)
    error_type = Column(String, nullable=True)
    misconception_tag = Column(String, nullable=True)

    response_time = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
