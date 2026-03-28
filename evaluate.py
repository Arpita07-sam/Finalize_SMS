import torch
import numpy as np
from sklearn.metrics import roc_curve
from torch.utils.data import DataLoader
from model import SiameseNetwork
from data_utils import prepare_data, generate_pairs, SignatureDataset

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def evaluate():
    data, _, val_writers, _ = prepare_data()
    val_pairs, val_labels = generate_pairs(data, val_writers)

    val_loader = DataLoader(
        SignatureDataset(val_pairs, val_labels),
        batch_size=32,
        shuffle=False
    )

    model = SiameseNetwork().to(DEVICE)
    model.load_state_dict(torch.load("siamese_model.pth", map_location=DEVICE))
    model.eval()

    distances = []
    labels = []

    with torch.no_grad():
        for img1, img2, label in val_loader:
            img1 = img1.to(DEVICE)
            img2 = img2.to(DEVICE)

            out1, out2 = model(img1, img2)
            dist = torch.nn.functional.pairwise_distance(out1, out2)

            distances.extend(dist.cpu().numpy())
            labels.extend(label.numpy())

    distances = np.array(distances)
    labels = np.array(labels)

    print("Distance Stats:")
    print("Min:", distances.min())
    print("Max:", distances.max())
    print("Mean:", distances.mean())

    print("Genuine mean distance:",
        distances[labels == 1].mean())

    print("Forged mean distance:",
        distances[labels == 0].mean())

    fpr, tpr, thresholds = roc_curve(labels, -distances)
    fnr = 1 - tpr

    idx = np.nanargmin(np.absolute(fnr - fpr))
    eer = fpr[idx]
    best_threshold = thresholds[idx]

    print("EER:", eer)
    print("Best Threshold:", best_threshold)


if __name__ == "__main__":
    evaluate()