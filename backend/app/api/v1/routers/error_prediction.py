from fastapi import APIRouter
from pydantic import BaseModel
from app.services.error_service import ErrorService

router = APIRouter()

class ErrorPredictionRequest(BaseModel):
    student_features: dict
    exercise_features: dict

@router.post("/")
def predict_error(req: ErrorPredictionRequest):
    """
    يتوقع الخطأ المحتمل قبل أن يحل الطالب المسألة.
    """
    result = ErrorService.predict_error(req.student_features, req.exercise_features)
    return result
