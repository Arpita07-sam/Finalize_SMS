import os

ORG_PATH = "signatures/full_org"

for file in os.listdir(ORG_PATH):
    parts = file.split("_")
    if len(parts) < 3:
        print("Problem file:", file)