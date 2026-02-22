import torch
import numpy as np
from sklearn.metrics import roc_curve
from model import SiameseNetwork

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = SiameseNetwork().to(DEVICE)
model.load_state_dict(torch.load("siamese_model.pth"))
model.eval()

print("Evaluation script ready.")