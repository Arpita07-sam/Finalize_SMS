import cv2
import os

def process_page(image_path, dept_id, count):
    output_folder = "static/signatures/cropped_signatures"
    os.makedirs(output_folder, exist_ok=True)

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    thresh = cv2.threshold(
        blur, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    saved_files = []
    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 80 and h > 30:   # adjust if needed
            crop = img[y:y+h, x:x+w]
            filename = f"{dept_id}_sign_{count+i}.png"
            save_path = os.path.join(output_folder, filename)
            cv2.imwrite(save_path, crop)
            saved_files.append(save_path)
    return saved_files


# # sign_cropper.py

# import cv2
# import os

# def process_page(image_path, dept_id):
#     output_folder = "static/signatures/cropped_signatures"
#     db_folder = "signatures/cropped_signatures"
#     os.makedirs(output_folder, exist_ok=True)
#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5,5), 0)
#     thresh = cv2.adaptiveThreshold(
#         blur, 255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY_INV,
#         15, 3
#     )
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,2))
#     remove_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,5))
#     dilated = cv2.dilate(thresh, kernel, iterations=1)
#     contours, _ = cv2.findContours(
#         dilated,
#         cv2.RETR_EXTERNAL,
#         cv2.CHAIN_APPROX_SIMPLE
#     )
#     count = 0
#     saved_paths = []
#     for c in contours:
#         x,y,w,h = cv2.boundingRect(c)
#         if w > 120 and h > 40:
#             crop = img[y:y+h, x:x+w]
#             filename = f"{dept_id}_sign_{count}.png"
#             save_path = os.path.join(output_folder, filename)
#             db_path = os.path.join(db_folder, filename)
#             cv2.imwrite(save_path, crop)
#             saved_paths.append(db_path)
#             count += 1
#     print("saved:", count)
#     return saved_paths