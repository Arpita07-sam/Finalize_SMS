import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms

from model import SiameseNetwork

# -----------------------------
# Device
# -----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# Load Model
# -----------------------------
model = SiameseNetwork().to(device)
model.load_state_dict(torch.load("best_model.pth", map_location=device))
model.eval()

# -----------------------------
# Image Transform
# -----------------------------
transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# -----------------------------
# Load Images
# -----------------------------
def load_image(path):
    img = Image.open(path).convert("L")
    img = transform(img)
    return img.unsqueeze(0)

# CHANGE THESE PATHS  signatures\full_org
reference_path = "signatures/full_org/original_3_5.png"
test_path = "signatures/full_forg/forgeries_3_1.png"

img1 = load_image(reference_path).to(device)
img2 = load_image(test_path).to(device)

# -----------------------------
# Compute Embeddings
# -----------------------------
with torch.no_grad():
    emb1 = model.forward_once(img1)
    emb2 = model.forward_once(img2)

distance = F.pairwise_distance(emb1, emb2).item()

print(f"Distance Score: {distance:.4f}")

# -----------------------------
# Decision Threshold
# -----------------------------
THRESHOLD = 0.55   # adjust later

if distance < THRESHOLD:
    print("✅ Signature VERIFIED")
else:
    print("❌ Likely FORGED")