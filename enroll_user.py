# import os
# import torch
# from PIL import Image
# import torchvision.transforms as transforms
# from model import SiameseNetwork
# import numpy as np

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = SiameseNetwork().to(device)
# model.load_state_dict(torch.load("best_model.pth", map_location=device))
# model.eval()


# base_transform = transforms.Compose([
#     transforms.Resize((128,128)),
# ])

# augmentation = transforms.Compose([
#     transforms.RandomRotation(5),
#     transforms.RandomAffine(
#         degrees=0,
#         translate=(0.03,0.03),
#         scale=(0.95,1.05)
#     )
# ])

# tensor_transform = transforms.Compose([
#     transforms.ToTensor(),
#     transforms.Normalize((0.5,), (0.5,))
# ])

# transform = transforms.Compose([
#     transforms.Resize((128,128)),
#     transforms.ToTensor(),
#     transforms.Normalize((0.5,), (0.5,))
# ])


# def get_embeddings(path, augment_times=5):

#     img = Image.open(path).convert("L")
#     img = base_transform(img)

#     embeddings = []

#     for _ in range(augment_times):

#         aug_img = augmentation(img)
#         aug_img = tensor_transform(aug_img)
#         aug_img = aug_img.unsqueeze(0).to(device)

#         with torch.no_grad():
#             emb = model.forward_once(aug_img)

#         embeddings.append(emb.cpu().numpy())

#     return embeddings




# user_name = "staff4"
# save_dir = f"office_database/{user_name}"
# os.makedirs(save_dir, exist_ok=True)

# signature_folder = "signatures/new_writers"

# count = 0

# for file in os.listdir(signature_folder):

#     path = os.path.join(signature_folder, file)

#     if not os.path.isfile(path):
#         continue

#     embs = get_embeddings(path)

#     for emb in embs:
#         np.save(f"{save_dir}/{file}_aug{count}.npy", emb)
#         # np.save(f"{save_dir}/emb_{count}.npy", emb)
#         count += 1

# import torch
# import torch.nn.functional as F
# import numpy as np

# all_embeddings = []

# for file in os.listdir(save_dir):
#     emb = np.load(os.path.join(save_dir, file))
#     all_embeddings.append(torch.tensor(emb))

# distances = []

# for i in range(len(all_embeddings)):
#     for j in range(i+1, len(all_embeddings)):
#         d = F.pairwise_distance(
#             all_embeddings[i],
#             all_embeddings[j]
#         ).item()
#         distances.append(d)

# mean_genuine = np.mean(distances)
# std_genuine = np.std(distances)

# print("User Mean Distance:", mean_genuine)
# print("User Std:", std_genuine)

# np.save(f"{save_dir}/threshold.npy",
#         np.array([mean_genuine, std_genuine]))


# print("User enrolled successfully!")

import os
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms
from model import SiameseNetwork

# ---------------- DEVICE ----------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------- MODEL ----------------
model = SiameseNetwork().to(device)
model.load_state_dict(torch.load("best_model.pth", map_location=device))
model.eval()

# ---------------- TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# =====================================================
# EMBEDDING FUNCTION (SAFE VERSION)
# =====================================================
def get_embedding(path):

    img = Image.open(path).convert("L")
    img = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        emb = model.forward_once(img)

    emb = emb.cpu()
    emb = F.normalize(emb, p=2, dim=1)

    return emb.numpy()[0]


# ---------------- USER ----------------
user = "staff2"
enroll_folder = f"signatures/new_writers"
save_path = f"office_database/{user}"

os.makedirs(save_path, exist_ok=True)

embeddings = []

# =====================================================
# CREATE NORMALIZED EMBEDDINGS
# =====================================================
for file in os.listdir(enroll_folder):

    if file.lower().endswith((".png",".jpg",".jpeg")):
        path = os.path.join(enroll_folder, file)

        emb = get_embedding(path)
        embeddings.append(emb)

embeddings = np.array(embeddings)

print("Total samples:", len(embeddings))

# =====================================================
# SAVE ALL EMBEDDINGS (DEBUG PURPOSE)
# =====================================================
np.save(f"{save_path}/all_embeddings.npy", embeddings)

# =====================================================
# PROTOTYPE
# =====================================================
prototype = np.mean(embeddings, axis=0)

# ⭐ VERY IMPORTANT
prototype = prototype / np.linalg.norm(prototype)

np.save(f"{save_path}/prototype.npy", prototype)

# =====================================================
# THRESHOLD
# =====================================================
distances = np.linalg.norm(embeddings - prototype, axis=1)

mean_genuine = np.mean(distances)
std_genuine = np.std(distances)

np.save(
    f"{save_path}/threshold.npy",
    np.array([mean_genuine, std_genuine])
)

print("\n✅ Enrollment Complete")
print("Mean:", mean_genuine)
print("Std:", std_genuine)
