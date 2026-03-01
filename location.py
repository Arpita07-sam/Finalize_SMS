from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="signature.yaml",
    epochs=50,
    imgsz=640
)

model = YOLO("best.pt")

results = model("test_document.jpg")

for r in results:
    boxes = r.boxes.xyxy

    for box in boxes:
        x1,y1,x2,y2 = map(int, box)

        img = cv2.imread("test_document.jpg")
        crop = img[y1:y2, x1:x2]

        cv2.imwrite("signature_crop.png", crop)