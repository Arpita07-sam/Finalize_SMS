# import numpy as np
# import torch
# import torch.nn.functional as F

# prototype = torch.tensor(
#     np.load("office_database/staff5/prototype.npy")
# ).unsqueeze(0)

# genuine = np.load("office_database/staff5/threshold.npy")

# dists = []

# for emb in genuine:
#     emb = torch.tensor(emb).unsqueeze(0)
#     d = F.pairwise_distance(emb, prototype).item()
#     dists.append(d)

# print("MIN:", np.min(dists))
# print("MAX:", np.max(dists))
# print("MEAN:", np.mean(dists))

import numpy as np
import torch

emb = np.load("office_database/staff2/all_embeddings.npy")

norms = []

for e in emb:
    norms.append(torch.norm(torch.tensor(e)).item())

print("Embedding norms:")
print("MIN:", min(norms))
print("MAX:", max(norms))
print("MEAN:", sum(norms)/len(norms))