import cv2
import os

image_path = "sign_page.jpeg"
output_folder = "cropped_signatures"
os.makedirs(output_folder, exist_ok=True)

img = cv2.imread(image_path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# remove noise
blur = cv2.GaussianBlur(gray, (5,5), 0)

# adaptive threshold (better for uneven lighting)
thresh = cv2.adaptiveThreshold(
    blur, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    15, 3
)

# remove thin lines (table borders)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,2))
remove_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# merge signature strokes
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,5))
dilated = cv2.dilate(thresh, kernel, iterations=1)

# find contours
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

count = 0

for c in contours:
    x,y,w,h = cv2.boundingRect(c)

    # ignore small noise
    if w > 80 and h > 30:
        crop = img[y:y+h, x:x+w]

        cv2.imwrite(f"{output_folder}/signature_{count}.png", crop)
        count += 1

print("saved:", count)