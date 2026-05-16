from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class AffectDetector:
    """
    نموذج كشف الحالة الانفعالية للطالب:
    - خوف
    - إحباط
    - توتر
    - ثقة
    """

    def __init__(self):
        model_name = "cardiffnlp/twitter-roberta-base-emotion"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def predict(self, text: str):
        """
        يأخذ نص الطالب ويعيد احتمالات المشاعر.
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)
        return probs.detach().numpy().tolist()
