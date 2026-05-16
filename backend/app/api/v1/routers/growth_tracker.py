from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.dependencies.db import get_db
from app.services.growth_service import GrowthService

router = APIRouter()

@router.get("/{student_id}")
def get_growth(student_id: int, db: Session = Depends(get_db)):
    """
    يحلل تطور الطالب عبر الزمن.
    """
    metrics = GrowthService.compute_growth(db, student_id)
    return {"student_id": student_id, "growth_metrics": metrics}
