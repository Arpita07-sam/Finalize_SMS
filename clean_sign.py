# import cv2
# import numpy as np

# # Load image
# img = cv2.imread("extracted_signature.jpg")

# if img is None:
#     print("Image not found")
#     exit()

# # Convert to HSV
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# # Green ink range
# lower_green = np.array([30, 20, 20])
# upper_green = np.array([100, 255, 255])

# mask = cv2.inRange(hsv, lower_green, upper_green)

# # Clean noise
# kernel = np.ones((3,3), np.uint8)

# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
# mask = cv2.dilate(mask, kernel, iterations=1)
# # kernel = np.ones((3,3), np.uint8)
# # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
# # mask = cv2.dilate(mask, kernel, iterations=2)

# # Extract only signature strokes
# signature = cv2.bitwise_and(img, img, mask=mask)

# # Convert to grayscale
# gray = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)

# # Threshold to isolate strokes
# _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

# # Find contours
# contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# x_min, y_min = 9999, 9999
# x_max, y_max = 0, 0

# for c in contours:
#     area = cv2.contourArea(c)
#     if area > 400:
#         x,y,w,h = cv2.boundingRect(c)

#         x_min = min(x_min, x)
#         y_min = min(y_min, y)
#         x_max = max(x_max, x+w)
#         y_max = max(y_max, y+h)

# pad = 10

# x_min = max(0, x_min-pad)
# y_min = max(0, y_min-pad)
# x_max = min(img.shape[1], x_max+pad)
# y_max = min(img.shape[0], y_max+pad)

# clean = signature[y_min:y_max, x_min:x_max]

# clean = cv2.resize(clean,(224,224))

# clean = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY)

# _, clean = cv2.threshold(clean, 10, 255, cv2.THRESH_BINARY_INV)

# cv2.imwrite("clean_signature.jpg", clean)

# print("Signature cleaned and saved")

# cv2.imshow("Mask", mask)
# cv2.imshow("Signature", clean)

# cv2.waitKey(0)
# cv2.destroyAllWindows()


# import cv2
# import numpy as np

# def clean_signature(img):  # img is numpy array from cv2.imread
#     if img is None:
#         raise ValueError("Input image is None")
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     denoised = cv2.fastNlMeansDenoising(gray)
#     blurred = cv2.medianBlur(denoised, 3)
#     binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
#     cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
#     return cleaned

# # Usage
# cropped_sig = cv2.imread("extracted_signature.jpg")
# cleaned = clean_signature(cropped_sig)
# cv2.imwrite("cleaned_signature.jpg", cleaned)
# print("Cleaned signature saved!")


import cv2
import numpy as np

def clean_signature_with_line_removal(img):
    if img is None:
        raise ValueError("Input image is None")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray)
    blurred = cv2.medianBlur(denoised, 3)
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)  # INV for black sig on white
    
    # Detect edges for Hough lines
    edges = cv2.Canny(binary, 50, 150)
    
    # HoughLinesP for horizontal lines: short length, high threshold for straight lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
    line_mask = np.zeros(binary.shape, dtype=np.uint8)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y1 - y2) < 10:  # Horizontal-ish lines only
                cv2.line(line_mask, (x1, y1), (x2, y2), 255, 5)  # Thicken to cover line
    
    # Inpaint lines (TELEA fast)
    inpainted = cv2.inpaint(binary, line_mask, 3, cv2.INPAINT_TELEA)
    
    # Final morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    cleaned = cv2.morphologyEx(inpainted, cv2.MORPH_OPEN, kernel)  # Open to disconnect
    
    return cleaned

# Usage
cropped_sig = cv2.imread("extracted_signature.jpg")
cleaned = clean_signature_with_line_removal(cropped_sig)
cv2.imwrite("signature_no_line.jpg", cleaned)
cv2.imshow("Cleaned", cleaned)
cv2.waitKey(0)
cv2.destroyAllWindows()
