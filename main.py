import os
import random
from collections import defaultdict

# Paths
ORG_PATH = "signatures/full_org"
FORG_PATH = "signatures/full_forg"

# Function to extract writer ID
def extract_writer_id(filename):
    return filename.split("_")[1]

# Create dictionary
# {
#   writer_id:
#       {
#           "genuine": [paths],
#           "forged": [paths]
#       }
# }

data = defaultdict(lambda: {"genuine": [], "forged": []})

# Process genuine signatures
for file in os.listdir(ORG_PATH):
    writer_id = extract_writer_id(file)
    full_path = os.path.join(ORG_PATH, file)
    data[writer_id]["genuine"].append(full_path)

# Process forged signatures
for file in os.listdir(FORG_PATH):
    writer_id = extract_writer_id(file)
    full_path = os.path.join(FORG_PATH, file)
    data[writer_id]["forged"].append(full_path)

# Check writers
writers = sorted(list(data.keys()))
print("Total Writers:", len(writers))

# Shuffle writers (for randomness but reproducible)
random.seed(42)
random.shuffle(writers)

# Writer-wise split
train_split = int(0.7 * len(writers))
val_split = int(0.85 * len(writers))

train_writers = writers[:train_split]
val_writers = writers[train_split:val_split]
test_writers = writers[val_split:]

print("Train Writers:", len(train_writers))
print("Val Writers:", len(val_writers))
print("Test Writers:", len(test_writers))

# Sanity check
print("\nExample Writer Structure:")
example_writer = writers[0]
print("Writer ID:", example_writer)
print("Genuine Count:", len(data[example_writer]["genuine"]))
print("Forged Count:", len(data[example_writer]["forged"]))

import itertools

def generate_pairs(writer_list):
    pairs = []
    labels = []

    for writer in writer_list:
        genuine = data[writer]["genuine"]
        forged = data[writer]["forged"]

        # --- Positive pairs (genuine-genuine)
        positive_pairs = list(itertools.combinations(genuine, 2))

        # --- Negative pairs (genuine-forged)
        negative_pairs = []
        for g in genuine:
            for f in forged:
                negative_pairs.append((g, f))

        # Balance them
        min_len = min(len(positive_pairs), len(negative_pairs))
        positive_pairs = positive_pairs[:min_len]
        negative_pairs = negative_pairs[:min_len]

        # Add to dataset
        for p in positive_pairs:
            pairs.append(p)
            labels.append(1)

        for p in negative_pairs:
            pairs.append(p)
            labels.append(0)

    return pairs, labels


# Generate splits
train_pairs, train_labels = generate_pairs(train_writers)
val_pairs, val_labels = generate_pairs(val_writers)
test_pairs, test_labels = generate_pairs(test_writers)

print("\nTrain Pairs:", len(train_pairs))
print("Val Pairs:", len(val_pairs))
print("Test Pairs:", len(test_pairs))