import os
import random
from PIL import Image
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms
from collections import defaultdict

class SignatureTripletDataset(Dataset):
    def __init__(self, genuine_dir, forged_dir, writers, image_size=224):

        self.transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.RandomRotation(5),
            transforms.RandomAffine(degrees=0, translate=(0.05, 0.05)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

        self.genuine = defaultdict(list)
        self.forged = defaultdict(list)

        for img in os.listdir(genuine_dir):
            writer_id = img.split('_')[1]
            if writer_id in writers:
                self.genuine[writer_id].append(os.path.join(genuine_dir, img))

        for img in os.listdir(forged_dir):
            writer_id = img.split('_')[1]
            if writer_id in writers:
                self.forged[writer_id].append(os.path.join(forged_dir, img))

        self.writers = list(self.genuine.keys())

    def __len__(self):
        return 2000  # define arbitrary triplet count

    def __getitem__(self, idx):

        writer = random.choice(self.writers)

        anchor_path = random.choice(self.genuine[writer])
        positive_path = random.choice(self.genuine[writer])
        # negative_writer = random.choice([w for w in self.writers if w != writer])
        # negative_path = random.choice(self.genuine[negative_writer])
        # negative_path = random.choice(self.forged[writer])
        negatives = random.sample(self.forged[writer], 3)
        negative_path = negatives[0]   # temporary

        anchor = self.transform(Image.open(anchor_path).convert("L"))
        positive = self.transform(Image.open(positive_path).convert("L"))
        negative = self.transform(Image.open(negative_path).convert("L"))

        return anchor, positive, negative

import os
import random
from PIL import Image
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms

class SignaturePairDataset(Dataset):
    def __init__(self, genuine_dir, forged_dir, writers, image_size=224):

        self.transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

        self.genuine = {}
        self.forged = {}

        for img in os.listdir(genuine_dir):
            writer_id = img.split('_')[1]
            if writer_id in writers:
                self.genuine.setdefault(writer_id, []).append(
                    os.path.join(genuine_dir, img)
                )

        for img in os.listdir(forged_dir):
            writer_id = img.split('_')[1]
            if writer_id in writers:
                self.forged.setdefault(writer_id, []).append(
                    os.path.join(forged_dir, img)
                )

        self.writers = list(self.genuine.keys())

    def __len__(self):
        return 1000

    def __getitem__(self, idx):

        writer = random.choice(self.writers)

        # Genuine pair
        if random.random() < 0.5:
            img1 = random.choice(self.genuine[writer])
            img2 = random.choice(self.genuine[writer])
            label = 1
        else:
            img1 = random.choice(self.genuine[writer])
            img2 = random.choice(self.forged[writer])
            label = 0

        img1 = self.transform(Image.open(img1).convert("L"))
        img2 = self.transform(Image.open(img2).convert("L"))

        return img1, img2, torch.tensor(label, dtype=torch.float32)