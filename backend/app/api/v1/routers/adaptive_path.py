from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.dependencies.db import get_db
from app.models.student import Student
from app.services.adaptive_service import AdaptiveService

router = APIRouter()

@router.get("/{student_id}")
def get_adaptive_path(student_id: int, db: Session = Depends(get_db)):
    """
    يولّد مسار تعلم شخصي للطالب بناءً على التوأم العقلي.
    """
    student = db.query(Student).get(student_id)

    if not student or not student.cognitive_profile:
        return {"error": "No cognitive profile found. Build it first."}

    path = AdaptiveService.generate_path(db, student.cognitive_profile)
    return {"student_id": student_id, "adaptive_path": path}
