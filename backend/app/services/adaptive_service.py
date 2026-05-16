from sqlalchemy.orm import Session
from app.models.exercise import Exercise

class AdaptiveService:
    """
    يولّد مسار تعلم شخصي للطالب بناءً على:
    - المواضيع الضعيفة
    - مستوى الصعوبة
    - عدد الأخطاء
    """

    @staticmethod
    def generate_path(db: Session, cognitive_profile: dict, limit: int = 10):
        weak_topics = [t[0] for t in cognitive_profile.get("weak_topics", [])]

        if not weak_topics:
            weak_topics = ["algebra", "fractions"]

        exercises = (
            db.query(Exercise)
            .filter(Exercise.topic.in_(weak_topics))
            .order_by(Exercise.difficulty.asc())
            .limit(limit)
            .all()
        )

        return [
            {
                "exercise_id": ex.id,
                "topic": ex.topic,
                "difficulty": ex.difficulty,
                "type": "practice",
            }
            for ex in exercises
        ]
