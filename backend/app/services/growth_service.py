from sqlalchemy.orm import Session
from app.models.attempt import Attempt

class GrowthService:
    """
    يحلل تطور الطالب عبر الزمن:
    - الدقة
    - سرعة التحسن
    - مقارنة البداية بالنهاية
    """

    @staticmethod
    def compute_growth(db: Session, student_id: int):
        attempts = (
            db.query(Attempt)
            .filter(Attempt.student_id == student_id)
            .order_by(Attempt.created_at.asc())
            .all()
        )

        if not attempts:
            return {"message": "No attempts found"}

        total = len(attempts)
        correct = sum(1 for a in attempts if a.is_correct)
        accuracy = correct / total

        k = max(1, total // 5)
        early = attempts[:k]
        late = attempts[-k:]

        early_acc = sum(1 for a in early if a.is_correct) / len(early)
        late_acc = sum(1 for a in late if a.is_correct) / len(late)

        return {
            "total_attempts": total,
            "overall_accuracy": accuracy,
            "early_accuracy": early_acc,
            "late_accuracy": late_acc,
            "improvement": late_acc - early_acc,
        }
