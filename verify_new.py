# import numpy as np
# import torch
# import torch.nn.functional as F
# from PIL import Image
# import torchvision.transforms as transforms
# from model import SiameseNetwork
# import os

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = SiameseNetwork().to(device)
# model.load_state_dict(torch.load("best_model.pth", map_location=device))
# model.eval()

# transform = transforms.Compose([
#     transforms.Resize((128,128)),
#     transforms.ToTensor(),
#     transforms.Normalize((0.5,), (0.5,))
# ])

# def get_embedding(path):
#     img = Image.open(path).convert("L")
#     img = transform(img).unsqueeze(0).to(device)

#     with torch.no_grad():
#         emb = model.forward_once(img)

#     return emb

# test_signature = "signatures/reference/ref23.jpeg"
# test_emb = get_embedding(test_signature)

# user = "staff2"
# db_path = f"office_database/{user}"

# stats = np.load(f"{db_path}/threshold.npy")

# mean_genuine = stats[0]
# std_genuine = stats[1]

# VERIFY_THRESHOLD = mean_genuine + 2 * std_genuine
# UNKNOWN_THRESHOLD = mean_genuine + 4 * std_genuine

# distances = []


# for file in os.listdir(db_path):

#     if not file.endswith(".npy"):
#         continue

#     if file == "threshold.npy":
#         continue   # 🔥 skip statistics file

#     ref = np.load(os.path.join(db_path, file))
#     ref = torch.tensor(ref).to(device)

#     d = F.pairwise_distance(test_emb, ref).item()
#     distances.append(d)



# THRESHOLD_MATCH = 0.55
# # MATCH_REQUIRED = 8
# # UNKNOWN_THRESHOLD = 0.65

# distances = np.array(distances)

# sorted_dist = np.sort(distances)

# TOP_K = 5
# best_k = sorted_dist[:TOP_K]

# mean_best = np.mean(best_k)

# print("Best K Mean:", mean_best)

# mean_distance = np.mean(distances)
# good_matches = np.sum(distances < THRESHOLD_MATCH)

# print("Mean Distance:", mean_distance)
# print("Good Matches:", good_matches)

# VERIFY_THRESHOLD = 0.55
# # UNKNOWN_THRESHOLD = 0.75

# if mean_best > UNKNOWN_THRESHOLD:
#     print("🚫 Unknown User")

# elif mean_best < VERIFY_THRESHOLD:
#     print("✅ Verified")

# else:
#     print("❌ Likely Forged")

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms
from model import SiameseNetwork

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SiameseNetwork().to(device)
model.load_state_dict(torch.load("best_model.pth", map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# ------------------------------------------------
def get_embedding(path):

    img = Image.open(path).convert("L")
    img = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        emb = model.forward_once(img)

    emb = emb.cpu()
    emb = F.normalize(emb, p=2, dim=1)

    return emb


# ---------------- INPUT ----------------
test_signature = "signatures/full_forg/forgeries_3_6.png"
user = "staff2"

db = f"office_database/{user}"

# ---------------- LOAD DATA ----------------
prototype = np.load(f"{db}/prototype.npy")
prototype = prototype / np.linalg.norm(prototype)

prototype = torch.tensor(prototype)\
            .unsqueeze(0)\
            .to(device)

mean_genuine, std_genuine = np.load(
    f"{db}/threshold.npy"
)

VERIFY_THRESHOLD = mean_genuine + 2*std_genuine
UNKNOWN_THRESHOLD = mean_genuine + 4*std_genuine

# ---------------- TEST ----------------
test_emb = get_embedding(test_signature)

distance = F.pairwise_distance(
    test_emb,
    prototype
).item()

print("\nImage:", test_signature)
print("\nDistance:", distance)
print("Verify Th:", VERIFY_THRESHOLD)
print("Unknown Th:", UNKNOWN_THRESHOLD)

# ---------------- DECISION ----------------
if distance > UNKNOWN_THRESHOLD:
    print("🚫 Unknown User")

elif distance < VERIFY_THRESHOLD:
    print("✅ Genuine")

else:
    print("❌ Forged")

