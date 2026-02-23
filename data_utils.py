import os
import random
import itertools
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset
from collections import defaultdict

ORG_PATH = "signatures/full_org"
FORG_PATH = "signatures/full_forg"


def extract_writer_id(filename):
    return filename.split("_")[1]


def prepare_data():
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
    test_writers = writers[val_split:]

    return data, train_writers, val_writers, test_writers


def generate_pairs(data, writer_list):
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