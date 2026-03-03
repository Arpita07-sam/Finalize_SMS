# import cv2
# import numpy as np
# import os

# # 1. Load Image
# img = cv2.imread(r"signatures\location\loc1.jpeg")
# if img is None:
#     print("Image not found")
#     exit()

# # 2. Fix Lighting (CLAHE)
# # This makes the green ink more distinct from the shadows on the paper
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# h, s, v = cv2.split(hsv)
# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
# v = clahe.apply(v)
# hsv = cv2.merge([h, s, v])

# # 3. Detect Green Ink (Widened Range)
# lower_green = np.array([35, 40, 40]) 
# upper_green = np.array([95, 255, 255])
# mask = cv2.inRange(hsv, lower_green, upper_green)

# # 4. Bridge the Gaps (Crucial for Photographs)
# # We use a larger kernel to join the individual pen strokes into one "blob"
# kernel = np.ones((15, 15), np.uint8) 
# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
# mask = cv2.dilate(mask, kernel, iterations=1)

# # 5. Find Contours and Crop
# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# if contours:
#     # Find the largest green area (the signature)
#     largest_cnt = max(contours, key=cv2.contourArea)
#     x, y, w, h = cv2.boundingRect(largest_cnt)

#     # Add a little padding so the crop isn't too tight
#     pad = 20
#     # Ensure padding doesn't go outside image boundaries
#     crop_img = img[max(0, y-pad):min(img.shape[0], y+h+pad), 
#                    max(0, x-pad):min(img.shape[1], x+w+pad)]
    
#         # 1. Convert the cropped image to HSV
#     crop_hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

#     # 2. Define the green range (same as before)
#     lower_green = np.array([35, 40, 40])
#     upper_green = np.array([95, 255, 255])

#     # 3. Create a mask of ONLY the green signature
#     sig_mask = cv2.inRange(crop_hsv, lower_green, upper_green)

#     # 4. Clean up the mask (remove noise, bridge small gaps in pen ink)
#     kernel = np.ones((3,3), np.uint8)
#     sig_mask = cv2.morphologyEx(sig_mask, cv2.MORPH_CLOSE, kernel)

#     # 5. Create a pure white background of the same size
#     white_bg = np.full(crop_img.shape, 255, dtype=np.uint8)

#     # 6. Copy only the green parts from the original crop onto the white background
#     # Where the mask is 255 (green found), use original pixels. Else, keep white.
#     final_signature = np.where(sig_mask[:, :, None] == 255, crop_img, white_bg)

#     # Save the cleaned signature
#     cv2.imwrite("only_signature.jpg", final_signature)

#     cv2.imshow("Cleaned Signature", final_signature)
#     cv2.waitKey(0)

#     # # 6. Save the Result
#     # save_path = "extracted_signature.jpg"
#     # cv2.imwrite(save_path, crop_img)
#     # print(f"Success! Signature saved as {save_path}")

#     # # Show the crop for verification
#     # cv2.imshow("Cropped Signature", crop_img)
#     # cv2.waitKey(0)
# else:
#     print("No signature detected. Check your HSV ranges.")

# cv2.destroyAllWindows()




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
