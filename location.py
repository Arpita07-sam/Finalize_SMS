
import cv2
import numpy as np
import os

# 1. Load Image
img = cv2.imread(r"signatures\location\loc6.jpeg")
if img is None:
    print("Image not found")
    exit()

# 2. Fix Lighting (CLAHE)
# This makes the green ink more distinct from the shadows on the paper
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
v = clahe.apply(v)
hsv = cv2.merge([h, s, v])

# 3. Detect Green Ink (Widened Range)
lower_green = np.array([35, 40, 40]) 
upper_green = np.array([95, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)

# 4. Bridge the Gaps (Crucial for Photographs)
# We use a larger kernel to join the individual pen strokes into one "blob"
kernel = np.ones((15, 15), np.uint8) 
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.dilate(mask, kernel, iterations=1)

# 5. Find Contours and Crop
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    # Find the largest green area (the signature)
    largest_cnt = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_cnt)

    # Add a little padding so the crop isn't too tight
    pad = 20
    # Ensure padding doesn't go outside image boundaries
    crop_img = img[max(0, y-pad):min(img.shape[0], y+h+pad), 
                   max(0, x-pad):min(img.shape[1], x+w+pad)]

    # 6. Save the Result
    save_path = "extracted_signature.jpg"
    cv2.imwrite(save_path, crop_img)
    print(f"Success! Signature saved as {save_path}")

    # Show the crop for verification
    cv2.imshow("Cropped Signature", crop_img)
    cv2.waitKey(0)
else:
    print("No signature detected. Check your HSV ranges.")

cv2.destroyAllWindows()

# import cv2
# import numpy as np

# # ---------- LOAD IMAGE ----------
# img = cv2.imread("signatures\location\loc6.jpeg")

# if img is None:
#     print("Image not found")
#     exit()

# original = img.copy()

# # # ---------- SIGNATURE DETECTION ----------
# # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# # # green ink range
# # lower_green = np.array([35, 40, 40])
# # upper_green = np.array([90, 255, 255])

# # mask = cv2.inRange(hsv, lower_green, upper_green)

# # kernel = np.ones((5,5), np.uint8)
# # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

# # contours, _ = cv2.findContours(
# #     mask,
# #     cv2.RETR_EXTERNAL,
# #     cv2.CHAIN_APPROX_SIMPLE
# # )

# # 1. Convert to Lab or HSV and Normalize Lighting
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# h, s, v = cv2.split(hsv)

# # Apply CLAHE to the Value channel to fix uneven lighting/shadows
# clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
# v = clahe.apply(v)
# hsv_normalized = cv2.merge([h, s, v])

# # 2. Refined Green Range (Widened for shadow/highlight variance)
# lower_green = np.array([35, 30, 30])   # Lowered saturation/value floor
# upper_green = np.array([95, 255, 255])

# mask = cv2.inRange(hsv_normalized, lower_green, upper_green)

# # 3. Aggressive Noise Removal & Connection
# # Use a bigger kernel or more iterations for photos
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
# mask = cv2.medianBlur(mask, 5) # Remove small speckles (sensor noise)

# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # ---------- DRAW SIGNATURE BOX ----------
# for cnt in contours:
#     area = cv2.contourArea(cnt)

#     if area > 500:
#         x, y, w, h = cv2.boundingRect(cnt)
#         cv2.rectangle(original, (x,y), (x+w,y+h), (0,0,255), 3)

# screen_width = 1400
# screen_height = 800

# h, w = original.shape[:2]

# scale_w = screen_width / w
# scale_h = screen_height / h

# scale = min(scale_w, scale_h)

# new_w = int(w * scale)
# new_h = int(h * scale)

# resized = cv2.resize(original, (new_w, new_h))


# # ---------- RESIZABLE WINDOW ----------
# cv2.namedWindow(
#     "Full Document - Signature Detection",
#     cv2.WINDOW_NORMAL
# )

# cv2.imshow("Full Document - Signature Detection", resized)

# cv2.waitKey(0)
# cv2.destroyAllWindows()


