import os

root = "/Users/neeru/PycharmProjects/Yolov8/cubicasa5k"
val_txt_path = os.path.join(root, "val.txt")

img_root = os.path.join(root, "high_quality")
lbl_root = os.path.join(root, "labels", "high_quality")

valid_lines = []

with open(val_txt_path, "r") as f:
    for line in f:
        folder = line.strip().strip("/")  # e.g. /high_quality/13852/
        filename = folder.split("/")[-1]  # "13852"

        img_path = os.path.join(img_root, filename + ".png")
        lbl_path = os.path.join(lbl_root, filename + ".txt")

        if os.path.exists(img_path) and os.path.exists(lbl_path):
            valid_lines.append(line)

with open(os.path.join(root, "val_clean.txt"), "w") as f:
    f.writelines(valid_lines)

print(f"Filtered {len(valid_lines)} valid lines saved to val_clean.txt")
