from sqlalchemy.orm import Session
from app.models.attempt import Attempt
from app.models.student import Student

class CognitiveService:
    """
    يبني التوأم العقلي للطالب عبر تحليل:
    - الأخطاء
    - المواضيع الضعيفة
    - المفاهيم الخاطئة
    - عدد المحاولات
    """

    @staticmethod
    def build_profile(db: Session, student_id: int):
        attempts = (
            db.query(Attempt)
            .filter(Attempt.student_id == student_id)
            .order_by(Attempt.created_at.asc())
            .all()
        )

        if not attempts:
            return {"message": "No attempts found for this student"}

        topic_stats = {}
        misconceptions = {}

        for a in attempts:
            topic = getattr(a, "topic", "unknown")

            if topic not in topic_stats:
                topic_stats[topic] = {"total": 0, "wrong": 0}

            topic_stats[topic]["total"] += 1
            if not a.is_correct:
                topic_stats[topic]["wrong"] += 1

            if a.misconception_tag:
                misconceptions[a.misconception_tag] = misconceptions.get(a.misconception_tag, 0) + 1

        profile = {
            "weak_topics": sorted(
                topic_stats.items(),
                key=lambda x: x[1]["wrong"] / max(1, x[1]["total"]),
                reverse=True,
            ),
            "misconceptions": misconceptions,
            "total_attempts": len(attempts),
        }

        student = db.query(Student).get(student_id)
        student.cognitive_profile = profile
        db.commit()

        return profile
