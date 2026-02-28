# 🏠 Floorplan-YOLO

Detect **walls, windows, and doors** in architectural floorplan images using YOLOv8.

## 📁 What's in here

| File | Purpose |
|---|---|
| `convert_svg_to_yolo.py` | Converts CubiCasa5K SVG annotations → YOLO `.txt` format |
| `train.py` | Trains YOLOv8n on the converted dataset |
| `hel.py` | Filters `val.txt` to only entries with valid image + label pairs |
| `yolov8n.pt` | Base YOLOv8 nano model (pre-trained on COCO) |
| `floorplan-test/` | Test images to run inference on |
| `floorplan-yolo/data.yaml` | Dataset config for YOLOv8 training |

## ⚡ Quickstart

```bash
pip install -r requirements.txt

# Step 1: Convert dataset annotations
python convert_svg_to_yolo.py

# Step 2: Train
python train.py
```

## 🗂 Dataset

Uses [CubiCasa5K](https://github.com/CubiCasa/CubiCasa5k) — 5,000 floor plan images with SVG annotations.

Set the `CUBICASA_ROOT` env variable to point to your dataset:
```bash
export CUBICASA_ROOT=/path/to/cubicasa5k
```

## 🏷️ Classes

| ID | Class |
|---|---|
| 0 | wall |
| 1 | window |
| 2 | door |
