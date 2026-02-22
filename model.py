import torch
import torch.nn as nn
import torch.nn.functional as F

class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()

        self.cnn = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 19 * 27, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 128)
        )

    def forward_once(self, x):
        x = self.cnn(x)
        x = self.fc(x)
        return F.normalize(x, p=2, dim=1)

    def forward(self, x1, x2):
        return self.forward_once(x1), self.forward_once(x2)


class ContrastiveLoss(nn.Module):
    def __init__(self, margin=1.0):
        super().__init__()
        self.margin = margin

    def forward(self, out1, out2, label):
        distance = F.pairwise_distance(out1, out2)
        loss = torch.mean(
            label * torch.pow(distance, 2) +
            (1 - label) * torch.pow(
                torch.clamp(self.margin - distance, min=0.0), 2
            )
        )
        return loss