import torch
import torch.nn as nn

class ErrorPredictor(nn.Module):
    """
    نموذج تصنيف الأخطاء الرياضية
    يأخذ ميزات الطالب + ميزات المسألة
    ويعطي احتمال كل نوع خطأ.
    """

    def __init__(self, input_dim=128, hidden_dim=256, num_classes=12):
        super().__init__()

        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(hidden_dim // 2, num_classes)
        )

    def forward(self, x):
        return self.model(x)
