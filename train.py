import os
import random
import itertools
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from collections import defaultdict
from model import SiameseNetwork, ContrastiveLoss

# CONFIG
ORG_PATH = "signatures/full_org"
FORG_PATH = "signatures/full_forg"
BATCH_SIZE = 32
EPOCHS = 15
LR = 0.0001
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", DEVICE)


# --------------------------
# DATA PREPARATION
# --------------------------
def extract_writer_id(filename):
    return filename.split("_")[1]


data = defaultdict(lambda: {"genuine": [], "forged": []})

for file in os.listdir(ORG_PATH):
    if file.endswith(".png"):
        wid = extract_writer_id(file)
        data[wid]["genuine"].append(os.path.join(ORG_PATH, file))

for file in os.listdir(FORG_PATH):
    if file.endswith(".png"):
        wid = extract_writer_id(file)
        data[wid]["forged"].append(os.path.join(FORG_PATH, file))

writers = list(data.keys())
random.seed(42)
random.shuffle(writers)

train_split = int(0.7 * len(writers))
val_split = int(0.85 * len(writers))

train_writers = writers[:train_split]
val_writers = writers[train_split:val_split]


def generate_pairs(writer_list):
    pairs = []
    labels = []

    for writer in writer_list:
        genuine = data[writer]["genuine"]
        forged = data[writer]["forged"]

        pos = list(itertools.combinations(genuine, 2))
        neg = [(g, f) for g in genuine for f in forged]

        min_len = min(len(pos), len(neg))
        pos = pos[:min_len]
        neg = neg[:min_len]

        for p in pos:
            pairs.append(p)
            labels.append(1)

        for p in neg:
            pairs.append(p)
            labels.append(0)

    return pairs, labels


train_pairs, train_labels = generate_pairs(train_writers)
val_pairs, val_labels = generate_pairs(val_writers)

train_pairs = train_pairs[:5000]
train_labels = train_labels[:5000]


# --------------------------
# DATASET
# --------------------------
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


# --------------------------
# TRAINING
# --------------------------
model = SiameseNetwork().to(DEVICE)
criterion = ContrastiveLoss(margin=1.0)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0

    for batch_idx, (img1, img2, label) in enumerate(train_loader):
        if batch_idx % 50 == 0:
            print(f"Epoch {epoch+1} Batch {batch_idx}")
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

torch.save(model.state_dict(), "siamese_model.pth")
print("Model saved.")

# import torch
# from torch.utils.data import DataLoader
# from model import SiameseNetwork, ContrastiveLoss
# from data_utils import prepare_data, generate_pairs, SignatureDataset

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# BATCH_SIZE = 32
# EPOCHS = 15
# LR = 0.0001


# def train():
#     data, train_writers, val_writers, _ = prepare_data()

#     train_pairs, train_labels = generate_pairs(data, train_writers)

#     train_loader = DataLoader(
#         SignatureDataset(train_pairs, train_labels),
#         batch_size=BATCH_SIZE,
#         shuffle=True
#     )

#     model = SiameseNetwork().to(DEVICE)
#     criterion = ContrastiveLoss()
#     optimizer = torch.optim.Adam(model.parameters(), lr=LR)

#     print("Using device:", DEVICE)

#     for epoch in range(EPOCHS):
#         model.train()
#         total_loss = 0

#         for batch_idx, (img1, img2, label) in enumerate(train_loader):
#             img1, img2, label = (
#                 img1.to(DEVICE),
#                 img2.to(DEVICE),
#                 label.to(DEVICE)
#             )

#             optimizer.zero_grad()
#             out1, out2 = model(img1, img2)
#             loss = criterion(out1, out2, label)
#             loss.backward()
#             optimizer.step()

#             total_loss += loss.item()

#             if batch_idx % 50 == 0:
#                 print(f"Epoch {epoch+1} Batch {batch_idx}")

#         print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {total_loss:.4f}")

#     torch.save(model.state_dict(), "siamese_model.pth")
#     print("Model saved.")


# if __name__ == "__main__":
#     train()