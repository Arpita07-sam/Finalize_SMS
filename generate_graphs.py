import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

distances = np.load("distances.npy")
labels = np.load("labels.npy")

scores = -distances   # smaller distance = genuine

fpr, tpr, thresholds = roc_curve(labels, scores)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
plt.plot([0,1],[0,1],'--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.grid()
plt.show()

fnr = 1 - tpr

plt.figure()
plt.plot(thresholds, fpr, label="FAR")
plt.plot(thresholds, fnr, label="FRR")
plt.xlabel("Threshold")
plt.ylabel("Error Rate")
plt.title("FAR vs FRR")
plt.legend()
plt.grid()
plt.show()

eer_index = np.nanargmin(np.absolute(fnr - fpr))
eer = fpr[eer_index]

plt.figure()
plt.plot(fpr, fnr)
plt.scatter(eer, eer, color='red', label=f"EER={eer:.3f}")
plt.xlabel("FAR")
plt.ylabel("FRR")
plt.title("Equal Error Rate Point")
plt.legend()
plt.grid()
plt.show()

print("EER:", eer)

genuine = distances[labels == 1]
forged = distances[labels == 0]

plt.figure()
plt.hist(genuine, bins=50, alpha=0.6, label="Genuine")
plt.hist(forged, bins=50, alpha=0.6, label="Forged")

plt.xlabel("Embedding Distance")
plt.ylabel("Frequency")
plt.title("Distance Distribution")
plt.legend()
plt.grid()
plt.show()