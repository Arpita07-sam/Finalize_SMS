import os
import random
import itertools
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from collections import defaultdict

# -----------------------------
# CONFIG
# -----------------------------
ORG_PATH = "signatures/full_org"
FORG_PATH = "signatures/full_forg"
BATCH_SIZE = 32
EPOCHS = 15
LR = 0.0001
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -----------------------------
# STEP 1 — LOAD DATA
# -----------------------------
def extract_writer_id(filename):
    return filename.split("_")[1]

data = defaultdict(lambda: {"genuine": [], "forged": []})

for file in os.listdir(ORG_PATH):
    if not file.endswith(".png"):
        continue
    writer_id = extract_writer_id(file)
    data[writer_id]["genuine"].append(os.path.join(ORG_PATH, file))

for file in os.listdir(FORG_PATH):
    if not file.endswith(".png"):
        continue
    writer_id = extract_writer_id(file)
    data[writer_id]["forged"].append(os.path.join(FORG_PATH, file))

writers = sorted(list(data.keys()))
random.seed(42)
random.shuffle(writers)

train_split = int(0.7 * len(writers))
val_split = int(0.85 * len(writers))

train_writers = writers[:train_split]
val_writers = writers[train_split:val_split]
test_writers = writers[val_split:]

print("Train:", len(train_writers),
      "Val:", len(val_writers),
      "Test:", len(test_writers))


# -----------------------------
# STEP 2 — PAIR GENERATION
# -----------------------------
def generate_pairs(writer_list):
    pairs = []
    labels = []

    for writer in writer_list:
        genuine = data[writer]["genuine"]
        forged = data[writer]["forged"]

        pos_pairs = list(itertools.combinations(genuine, 2))
        neg_pairs = [(g, f) for g in genuine for f in forged]

        min_len = min(len(pos_pairs), len(neg_pairs))
        pos_pairs = pos_pairs[:min_len]
        neg_pairs = neg_pairs[:min_len]

        for p in pos_pairs:
            pairs.append(p)
            labels.append(1)

        for p in neg_pairs:
            pairs.append(p)
            labels.append(0)

    return pairs, labels


train_pairs, train_labels = generate_pairs(train_writers)
val_pairs, val_labels = generate_pairs(val_writers)
test_pairs, test_labels = generate_pairs(test_writers)

print("Train pairs:", len(train_pairs))


# -----------------------------
# STEP 3 — DATASET
# -----------------------------
class SignatureDataset(Dataset):
    def __init__(self, pairs, labels):
        self.pairs = pairs
        self.labels = labels

    def preprocess(self, path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (220, 155))
        _, img = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        return torch.tensor(img, dtype=torch.float32)

    def __getitem__(self, idx):
        img1_path, img2_path = self.pairs[idx]
        label = self.labels[idx]

        img1 = self.preprocess(img1_path)
        img2 = self.preprocess(img2_path)

        return img1, img2, torch.tensor(label, dtype=torch.float32)

    def __len__(self):
        return len(self.pairs)


train_loader = DataLoader(
    SignatureDataset(train_pairs, train_labels),
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_loader = DataLoader(
    SignatureDataset(val_pairs, val_labels),
    batch_size=BATCH_SIZE,
    shuffle=False
)


# -----------------------------
# STEP 4 — MODEL
# -----------------------------
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
        out1 = self.forward_once(x1)
        out2 = self.forward_once(x2)
        return out1, out2


model = SiameseNetwork().to(DEVICE)


# -----------------------------
# STEP 5 — LOSS
# -----------------------------
class ContrastiveLoss(nn.Module):
    def __init__(self, margin=1.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, output1, output2, label):
        distance = F.pairwise_distance(output1, output2)
        loss = torch.mean(
            label * torch.pow(distance, 2) +
            (1 - label) * torch.pow(
                torch.clamp(self.margin - distance, min=0.0), 2
            )
        )
        return loss


criterion = ContrastiveLoss(margin=1.0)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)


# -----------------------------
# STEP 6 — TRAINING LOOP
# -----------------------------
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0

    for img1, img2, label in train_loader:
        img1, img2, label = (
            img1.to(DEVICE),
            img2.to(DEVICE),
            label.to(DEVICE)
        )

        optimizer.zero_grad()
        out1, out2 = model(img1, img2)
        loss = criterion(out1, out2, label)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {total_loss:.4f}")

print("Training Complete.")