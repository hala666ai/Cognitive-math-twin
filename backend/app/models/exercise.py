from sqlalchemy import Column, Integer, String, Float, JSON
from app.db_init import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    difficulty = Column(Float, default=0.5)
    metadata = Column(JSON, default={})  # skills المطلوبة، صيغة السؤال، إلخ
