import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from dataset import SignaturePairDataset
from model import SiameseNetwork

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Use ONLY validation writers for testing
test_writers = [str(i) for i in range(41,56)]

dataset = SignaturePairDataset(
    genuine_dir="signatures/full_org",
    forged_dir="signatures/full_forg",
    writers=test_writers
)

loader = DataLoader(dataset, batch_size=16, shuffle=False)

model = SiameseNetwork().to(device)
model.load_state_dict(torch.load("best_model.pth"))
model.eval()

all_labels = []
all_distances = []

with torch.no_grad():
    for img1, img2, labels in loader:

        img1 = img1.to(device)
        img2 = img2.to(device)

        emb1 = model.forward_once(img1)
        emb2 = model.forward_once(img2)

        distances = F.pairwise_distance(emb1, emb2)

        all_distances.extend(distances.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())


import numpy as np
from sklearn.metrics import roc_curve

all_distances = np.array(all_distances)
all_labels = np.array(all_labels)



np.save("distances.npy", all_distances)
np.save("labels.npy", all_labels)

print("Saved evaluation data")

# Try different thresholds
thresholds = np.linspace(min(all_distances), max(all_distances), 100)

best_acc = 0

for t in thresholds:
    preds = (all_distances < t).astype(int)
    acc = np.mean(preds == all_labels)
    if acc > best_acc:
        best_acc = acc

print("Test Accuracy:", best_acc)

# EER
fpr, tpr, thresholds = roc_curve(all_labels, -all_distances)
fnr = 1 - tpr
eer = fpr[np.nanargmin(np.absolute((fnr - fpr)))]
print("EER:", eer)