import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms
from model import SiameseNetwork
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SiameseNetwork().to(device)
model.load_state_dict(torch.load("best_model.pth", map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

def get_embedding(path):
    img = Image.open(path).convert("L")
    img = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        emb = model.forward_once(img)

    return emb


test_signature = "signatures/reference/ref23.jpeg"
test_emb = get_embedding(test_signature)

user = "staff2"
db_path = f"office_database/{user}"

stats = np.load(f"{db_path}/threshold.npy")

mean_genuine = stats[0]
std_genuine = stats[1]

VERIFY_THRESHOLD = mean_genuine + 2 * std_genuine
UNKNOWN_THRESHOLD = mean_genuine + 4 * std_genuine

distances = []

# for file in os.listdir(db_path):
#     ref = np.load(os.path.join(db_path,file))
#     ref = torch.tensor(ref).to(device)

#     d = F.pairwise_distance(test_emb, ref).item()
#     distances.append(d)

for file in os.listdir(db_path):

    if not file.endswith(".npy"):
        continue

    if file == "threshold.npy":
        continue   # 🔥 skip statistics file

    ref = np.load(os.path.join(db_path, file))
    ref = torch.tensor(ref).to(device)

    d = F.pairwise_distance(test_emb, ref).item()
    distances.append(d)



THRESHOLD_MATCH = 0.55
MATCH_REQUIRED = 8
UNKNOWN_THRESHOLD = 0.65

distances = np.array(distances)

sorted_dist = np.sort(distances)

TOP_K = 5
best_k = sorted_dist[:TOP_K]

mean_best = np.mean(best_k)

print("Best K Mean:", mean_best)

mean_distance = np.mean(distances)
good_matches = np.sum(distances < THRESHOLD_MATCH)

print("Mean Distance:", mean_distance)
print("Good Matches:", good_matches)

VERIFY_THRESHOLD = 0.55
# UNKNOWN_THRESHOLD = 0.75

if mean_best > UNKNOWN_THRESHOLD:
    print("🚫 Unknown User")

elif mean_best < VERIFY_THRESHOLD:
    print("✅ Verified")

else:
    print("❌ Likely Forged")

# if mean_best > UNKNOWN_THRESHOLD:
#     print("🚫 Unknown User")

# elif mean_best < VERIFY_THRESHOLD:
#     print("✅ Verified")

# else:
#     print("❌ Likely Forged")

# ------------------------------
# FINAL DECISION LOGIC
# ------------------------------

# if mean_distance > UNKNOWN_THRESHOLD:
#     print("🚫 Unknown User")

# elif good_matches >= MATCH_REQUIRED:
#     print("✅ Verified")

# else:
#     print("❌ Likely Forged")

# score = min(distances)

# print("Best Distance:", score)

# import numpy as np

# distances = np.array(distances)

# mean_distance = np.mean(distances)
# good_matches = np.sum(distances < 0.55)

# print("Mean Distance:", mean_distance)
# print("Good Matches:", good_matches)

# MATCH_REQUIRED = 8   # tune later

# if good_matches >= MATCH_REQUIRED:
#     print("✅ Verified")
# else:
#     print("❌ Forged / Unknown")

# if mean_distance > 0.65:
#     print("🚫 Unknown User")

# THRESHOLD = 0.55

# if score < THRESHOLD:
#     print("✅ Verified")
# else:
#     print("❌ Unknown / Forged")