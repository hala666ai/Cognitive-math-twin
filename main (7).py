from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time

app = FastAPI()

# السماح للفرونت إند يتصل بالباك إند
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تخزين بسيط بالذاكرة (تطوره لاحقاً لقاعدة بيانات)
students_sessions: Dict[str, Dict] = {}

class Step(BaseModel):
    step_text: str
    is_correct: bool
    timestamp: float

class SessionData(BaseModel):
    student_id: str
    problem_id: str
    steps: List[Step]

@app.post("/submit_session")
def submit_session(data: SessionData):
    # إذا ما في سجل للطالب، أنشئ واحد
    if data.student_id not in students_sessions:
        students_sessions[data.student_id] = {
            "sessions": [],
            "stats": {
                "total_steps": 0,
                "total_errors": 0,
                "concept_confusion": {},
            }
        }

    student = students_sessions[data.student_id]
    student["sessions"].append(data.dict())

    # تحديث الإحصائيات
    for step in data.steps:
        student["stats"]["total_steps"] += 1
        if not step.is_correct:
            student["stats"]["total_errors"] += 1
            # تحليل بسيط للكلمات لمعرفة نوع اللبس
            text = step.step_text.lower()
            if "fraction" in text or "كسر" in text:
                key = "fractions"
            elif "equation" in text or "معادلة" in text:
                key = "equations"
            elif "limit" in text or "نهاية" in text:
                key = "calculus"
            else:
                key = "general"

            if key not in student["stats"]["concept_confusion"]:
                student["stats"]["concept_confusion"][key] = 0
            student["stats"]["concept_confusion"][key] += 1

    return {"status": "ok", "message": "Session recorded successfully."}

@app.get("/profile/{student_id}")
def get_profile(student_id: str):
    if student_id not in students_sessions:
        return {"error": "Student not found."}

    student = students_sessions[student_id]
    stats = student["stats"]

    if stats["total_steps"] == 0:
        error_rate = 0.0
    else:
        error_rate = stats["total_errors"] / stats["total_steps"]

    # تحليل بسيط يعطي "بروفايل عقلي"
    profile = {
        "student_id": student_id,
        "total_sessions": len(student["sessions"]),
        "total_steps": stats["total_steps"],
        "total_errors": stats["total_errors"],
        "error_rate": round(error_rate, 2),
        "concept_confusion": stats["concept_confusion"],
        "ai_comment": generate_ai_comment(error_rate, stats["concept_confusion"])
    }

    return profile

def generate_ai_comment(error_rate: float, confusion: Dict[str, int]) -> str:
    if error_rate == 0:
        return "أنت تحل بثقة عالية جداً تقريباً بدون أخطاء. حان وقت تحديات أعلى!"
    if error_rate < 0.2:
        base = "أداؤك ممتاز، نسبة الأخطاء منخفضة."
    elif error_rate < 0.5:
        base = "أداؤك جيد لكن في مساحة لتحسين طريقة تفكيرك."
    else:
        base = "نسبة الأخطاء مرتفعة، وهذا طبيعي إذا كنت تتحدى نفسك بمسائل صعبة."

    if confusion:
        worst_concept = max(confusion, key=confusion.get)
        if worst_concept == "fractions":
            extra = "يبدو أن لديك لبس في الكسور. حاول التركيز على فهم معنى الكسر قبل الحساب."
        elif worst_concept == "equations":
            extra = "المعادلات تحتاج تنظيم خطوات أكثر. جرّب كتابة كل خطوة بوضوح."
        elif worst_concept == "calculus":
            extra = "مفاهيم النهايات والتفاضل تحتاج صبر وتكرار أمثلة بسيطة."
        else:
            extra = "هناك بعض الأخطاء العامة، حاول التمهل في كل خطوة."
    else:
        extra = "لا يوجد نمط واضح للأخطاء حتى الآن."

    return base + " " + extra

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)