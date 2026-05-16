import numpy as np
import torch
import torch.nn.functional as F
from app.ml.error_model import ErrorPredictor

# تحميل نموذج التنبؤ بالأخطاء
model = ErrorPredictor()
model.eval()

ERROR_LABELS = [
    "sign_error",
    "algebraic_simplification",
    "misapplied_formula",
    "conceptual_gap",
    "careless_mistake",
    "operation_order",
    "fraction_misunderstanding",
    "equation_setup",
    "geometry_misconception",
    "logic_error",
    "misreading_question",
    "other",
]

class ErrorService:
    """
    يتوقع الخطأ المحتمل قبل أن يحل الطالب المسألة.
    """

    @staticmethod
    def featurize(student_features: dict, exercise_features: dict):
        vec = np.zeros(128, dtype="float32")

        vec[0] = student_features.get("accuracy", 0.5)
        vec[1] = student_features.get("speed", 0.5)
        vec[2] = exercise_features.get("difficulty", 0.5)

        return torch.tensor(vec).unsqueeze(0)

    @staticmethod
    def predict_error(student_features: dict, exercise_features: dict):
        x = ErrorService.featurize(student_features, exercise_features)

        with torch.no_grad():
            logits = model(x)
            probs = F.softmax(logits, dim=1).squeeze(0).tolist()

        ranked = sorted(
            zip(ERROR_LABELS, probs),
            key=lambda x: x[1],
            reverse=True,
        )

        return {
            "predicted_error": ranked[0][0],
            "probability": ranked[0][1],
            "all_errors": [{"type": t, "prob": p} for t, p in ranked],
        }
