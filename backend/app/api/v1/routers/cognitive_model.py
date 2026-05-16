from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.dependencies.db import get_db
from app.services.cognitive_service import CognitiveService

router = APIRouter()

@router.post("/rebuild/{student_id}")
def rebuild_cognitive_model(student_id: int, db: Session = Depends(get_db)):
    """
    يعيد بناء التوأم العقلي للطالب عبر تحليل محاولاته السابقة.
    """
    profile = CognitiveService.build_profile(db, student_id)
    return {"student_id": student_id, "cognitive_profile": profile}
