# 🏠 Floorplan-YOLO

A **demo project** exploring YOLOv8 object detection applied to architectural floorplan images — detecting walls, windows, and doors.

> ⚠️ **This project was built purely for learning and demonstration purposes.**

---

## 📌 Disclaimer

This repository is an **educational experiment** and personal learning project. It is:

- **Not a commercial product** — built solely to explore computer vision and YOLOv8
- **Not affiliated with or endorsed by** CubiCasa or any related organization
- **Not intended for redistribution** of any dataset

### Dataset Notice

This project references the **CubiCasa5K** dataset for training purposes.

> The CubiCasa5K dataset is the property of [CubiCasa](https://github.com/CubiCasa/CubiCasa5k) and is subject to its own license terms.
> **This repository does NOT include, redistribute, or claim any rights over the CubiCasa5K dataset.**
> If you wish to use the dataset, please refer to the [original repository](https://github.com/CubiCasa/CubiCasa5k) and comply with their licensing terms.

The dataset is **not bundled here** — you must download it separately from the official source.

---

## 📁 What's in here

| File | Purpose |
|---|---|
| `convert_svg_to_yolo.py` | Converts CubiCasa5K SVG annotations → YOLO `.txt` format |
| `train.py` | Trains YOLOv8n on the converted dataset |
| `hel.py` | Filters `val.txt` to only entries with valid image + label pairs |
| `yolov8n.pt` | Base YOLOv8 nano model (pre-trained on COCO, by Ultralytics) |
| `floorplan-test/` | Sample test images for inference |
| `floorplan-yolo/data.yaml` | Dataset config for YOLOv8 training |

---

## ⚡ How to Run (Demo)

```bash
pip install -r requirements.txt

# Step 1: Download CubiCasa5K dataset from official source
# https://github.com/CubiCasa/CubiCasa5k

# Step 2: Point to your dataset
export CUBICASA_ROOT=/path/to/cubicasa5k

# Step 3: Convert annotations to YOLO format
python convert_svg_to_yolo.py

# Step 4: Train
python train.py
```

---

## 🏷️ What It Detects

| ID | Class |
|---|---|
| 0 | wall |
| 1 | window |
| 2 | door |

---

## 📄 License

This code is released for **educational/demo use only**.
The author makes no warranty and assumes no liability for any use of this code.
All dataset rights belong to their respective owners.
