# train.py

import torch
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn.functional as F

from dataset import SignatureTripletDataset
from model import SiameseNetwork

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ----------------------------
# 1️⃣ Split Writers
# ----------------------------
train_writers = [str(i) for i in range(1, 41)]
val_writers = [str(i) for i in range(41, 56)]

# ----------------------------
# 2️⃣ Create Datasets
# ----------------------------
train_dataset = SignatureTripletDataset(
    genuine_dir="CEDAR/full_org",
    forged_dir="CEDAR/full_forg",
    writers=train_writers
)

val_dataset = SignatureTripletDataset(
    genuine_dir="CEDAR/full_org",
    forged_dir="CEDAR/full_forg",
    writers=val_writers
)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

# ----------------------------
# 3️⃣ Model, Loss, Optimizer
# ----------------------------
model = SiameseNetwork().to(device)
criterion = torch.nn.TripletMarginLoss(margin=1.0)
optimizer = optim.Adam(model.parameters(), lr=1e-4)

# ----------------------------
# 4️⃣ Validation Function
# ----------------------------
def validate(model, loader):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for anchor, positive, negative in loader:

            anchor = anchor.to(device)
            positive = positive.to(device)
            negative = negative.to(device)

            a, p, n = model(anchor, positive, negative)
            loss = criterion(a, p, n)
            total_loss += loss.item()

            d_pos = F.pairwise_distance(a, p)
            d_neg = F.pairwise_distance(a, n)

            correct += torch.sum(d_pos < d_neg).item()
            total += anchor.size(0)

    avg_loss = total_loss / len(loader)
    accuracy = correct / total

    return avg_loss, accuracy

# ----------------------------
# 5️⃣ Training Loop
# ----------------------------
best_val_loss = float("inf")
patience = 5
counter = 0

for epoch in range(30):

    model.train()
    train_loss = 0

    for anchor, positive, negative in train_loader:

        anchor = anchor.to(device)
        positive = positive.to(device)
        negative = negative.to(device)

        optimizer.zero_grad()

        a, p, n = model(anchor, positive, negative)
        loss = criterion(a, p, n)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()

    train_loss /= len(train_loader)

    val_loss, val_acc = validate(model, val_loader)

    print(f"\nEpoch {epoch+1}")
    print(f"Train Loss: {train_loss:.4f}")
    print(f"Val Loss: {val_loss:.4f}")
    print(f"Val Accuracy: {val_acc:.4f}")
    print("-"*40)

    # Early Stopping
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(model.state_dict(), "best_model.pth")
        counter = 0
    else:
        counter += 1

    if counter >= patience:
        print("Early stopping triggered.")
        break