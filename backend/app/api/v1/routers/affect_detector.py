from fastapi import APIRouter
from pydantic import BaseModel
from app.services.affect_service import AffectService

router = APIRouter()

class AffectRequest(BaseModel):
    text: str

@router.post("/")
def detect_affect(req: AffectRequest):
    """
    يكشف الحالة الانفعالية للطالب (خوف، إحباط، توتر، ثقة).
    """
    result = AffectService.detect(req.text)
    return result
