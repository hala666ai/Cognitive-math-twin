import torch
import torch.nn as nn

class KnowledgeTracing(nn.Module):
    """
    نموذج تتبع المعرفة للطالب (Knowledge Tracing)
    يعتمد على LSTM لتحليل تسلسل إجابات الطالب
    وتوقع مستوى إتقانه للمهارات.
    """

    def __init__(self, num_skills: int, hidden_size: int = 256, num_layers: int = 2):
        super().__init__()

        # كل skill له حالتين: صح / خطأ → لذلك ×2
        self.embedding = nn.Embedding(num_skills * 2, hidden_size)

        self.lstm = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.25,
        )

        self.fc = nn.Linear(hidden_size, num_skills)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        """
        x: تسلسل إجابات الطالب (skill_id * 2 + correctness)
        """
        x = self.embedding(x)
        out, _ = self.lstm(x)
        out = self.fc(out)
        return self.sigmoid(out)
