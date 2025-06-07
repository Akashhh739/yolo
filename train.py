from ultralytics import YOLO
# Load model
model = YOLO("yolov8n.yaml")  # or yolov8s.yaml for slightly larger model

# Train it!
model.train(
    data="data.yaml",
    epochs=50,
    imgsz=640,
    batch=8
)
