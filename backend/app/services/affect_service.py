from app.ml.affect_model import AffectDetector

affect_model = AffectDetector()

class AffectService:
    """
    يكشف الحالة الانفعالية للطالب:
    - خوف
    - إحباط
    - توتر
    - ثقة
    """

    @staticmethod
    def detect(text: str):
        probs = affect_model.predict(text)[0]

        emotions = ["anger", "joy", "optimism", "sadness"]
        result = dict(zip(emotions, probs))

        dominant = max(result, key=result.get)

        return {
            "emotions": result,
            "dominant_emotion": dominant,
        }
