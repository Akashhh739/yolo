import os

# ── Config — set this to wherever your cubicasa5k dataset lives ──
ROOT = os.environ.get("CUBICASA_ROOT", "/Users/neeru/PycharmProjects/Yolov8/cubicasa5k")

val_txt_path = os.path.join(ROOT, "val.txt")
img_root = os.path.join(ROOT, "high_quality")
lbl_root = os.path.join(ROOT, "labels", "high_quality")

valid_lines = []

if not os.path.exists(val_txt_path):
    print(f"❌ val.txt not found at {val_txt_path}")
    print("Set the CUBICASA_ROOT environment variable to the dataset path.")
    exit(1)

with open(val_txt_path, "r") as f:
    for line in f:
        folder = line.strip().strip("/")   # e.g. high_quality/13852
        filename = folder.split("/")[-1]   # "13852"

        img_path = os.path.join(img_root, filename + ".png")
        lbl_path = os.path.join(lbl_root, filename + ".txt")

        if os.path.exists(img_path) and os.path.exists(lbl_path):
            valid_lines.append(line)

with open(os.path.join(ROOT, "val_clean.txt"), "w") as f:
    f.writelines(valid_lines)

print(f"✅ Filtered {len(valid_lines)} valid lines saved to val_clean.txt")
