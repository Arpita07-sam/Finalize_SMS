# import cv2
# import numpy as np

# # ---------------- SETTINGS ---------------- #

# # threshold to decide recoverable or not
# RECOVERY_THRESHOLD = 0.40   # change if needed


# # ---------------- STEP 1: GREEN DETECTION ---------------- #

# def detect_green_signature(img):

#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     # green ink range (tune if needed)
#     lower_green = np.array([35, 40, 40])
#     upper_green = np.array([90, 255, 255])

#     green_mask = cv2.inRange(hsv, lower_green, upper_green)

#     # clean noise
#     kernel = np.ones((3,3), np.uint8)
#     green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

#     return green_mask


# # ---------------- STEP 2: PRINTED TEXT DETECTION ---------------- #

# # def detect_printed_text(img):

# #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# #     # threshold for dark text
# #     _, text_mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

# #     # remove thick areas (signature strokes)
# #     kernel = np.ones((2,2), np.uint8)
# #     text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, kernel)

# #     return text_mask

# def detect_printed_text(img):

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # adaptive threshold works better for printed text
#     text_mask = cv2.adaptiveThreshold(
#         gray, 255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY_INV,
#         11, 2
#     )

#     # remove noise (very important)
#     kernel = np.ones((2,2), np.uint8)
#     text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, kernel)

#     return text_mask


# # ---------------- STEP 3 + 4 + 5 PIPELINE ---------------- #

# def recover_signature(img):

#     green_mask = detect_green_signature(img)
#     text_mask = detect_printed_text(img)

#     # overlap region
#     overlap = cv2.bitwise_and(green_mask, text_mask)

#     # area calculation
#     sig_area = np.sum(green_mask > 0)
#     overlap_area = np.sum(overlap > 0)

#     if sig_area == 0:
#         return "NO SIGNATURE FOUND", None

#     erased_ratio = overlap_area / sig_area

#     print("Signature area:", sig_area)
#     print("Overlap area:", overlap_area)
#     print("Erased ratio:", erased_ratio)

#     cv2.imshow("Green Mask", green_mask)
#     cv2.imshow("Text Mask", text_mask)
#     cv2.imshow("Overlap", overlap)
#     # cv2.waitKey(0)

#     # decision
#     if erased_ratio > RECOVERY_THRESHOLD:
#         return "NOT POSSIBLE", None

#     # recover using inpainting
#     recovered = cv2.inpaint(img, overlap, 3, cv2.INPAINT_TELEA)

#     return "RECOVERED", recovered


# # ---------------- RUN ---------------- #

# img = cv2.imread("extracted_signature.jpg")

# status, result = recover_signature(img)

# print("STATUS:", status)



# if result is not None:
#     cv2.imshow("Recovered Signature", result)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

import cv2
import numpy as np

RECOVERY_THRESHOLD = 0.40


def detect_green_signature(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # ✅ relaxed green range (important)
    lower_green = np.array([25, 20, 20])
    upper_green = np.array([95, 255, 255])

    mask1 = cv2.inRange(hsv, lower_green, upper_green)

    # ✅ also detect faint strokes using color difference
    b, g, r = cv2.split(img)

    diff = cv2.subtract(g, r)
    _, mask2 = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)

    # combine both
    green_mask = cv2.bitwise_or(mask1, mask2)

    # clean noise
    kernel = np.ones((3,3), np.uint8)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

    return green_mask


def detect_printed_text(img, green_mask):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # detect dark printed text only
    _, dark_mask = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)

    # remove signature area
    dark_mask[green_mask > 0] = 0

    kernel = np.ones((2,2), np.uint8)
    dark_mask = cv2.morphologyEx(dark_mask, cv2.MORPH_OPEN, kernel)

    return dark_mask


# ---------- MAIN PIPELINE ---------- #

def recover_signature(img):

    green_mask = detect_green_signature(img)
    text_mask = detect_printed_text(img, green_mask)

    overlap = cv2.bitwise_and(green_mask, text_mask)

    sig_area = np.sum(green_mask > 0)
    overlap_area = np.sum(overlap > 0)

    if sig_area == 0:
        return "NO SIGNATURE FOUND", None

    erased_ratio = overlap_area / sig_area

    print("Signature area:", sig_area)
    print("Overlap area:", overlap_area)
    print("Erased ratio:", erased_ratio)

    # decision
    if erased_ratio > RECOVERY_THRESHOLD:
        return "NOT POSSIBLE", None

    recovered = cv2.inpaint(img, overlap, 3, cv2.INPAINT_TELEA)

    # debug (VERY IMPORTANT)
    cv2.imshow("Green Mask", green_mask)
    cv2.imshow("Text Mask", text_mask)
    cv2.imshow("Overlap", overlap)
    cv2.imshow("Recovered", recovered)
    # cv2.waitKey(0)

    return "RECOVERED", recovered

def preprocess_for_model(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (224,224))   # match training size
    gray = gray / 255.0
    return gray

def extract_only_signature(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # threshold for signature strokes
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    # find bounding box
    coords = cv2.findNonZero(thresh)
    x, y, w, h = cv2.boundingRect(coords)
    cropped = img[y:y+h, x:x+w]
    return cropped


# ---------- RUN ---------- #

img = cv2.imread("extracted_signature.jpg")

status, result = recover_signature(img)

print("STATUS:", status)

if status == "RECOVERED":
    sig_only = extract_only_signature(result)
    processed = preprocess_for_model(result)
    cv2.imshow("Preprocessed", processed)
    cv2.waitKey(0)
else:
    print("Signature not usable")



