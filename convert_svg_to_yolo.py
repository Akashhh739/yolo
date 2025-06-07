import os
import shutil
import xml.etree.ElementTree as ET
from PIL import Image

# === Config ===
ROOT = "cubicasa5k"  # root folder containing all subfolders with images + svg
OUT_IMAGES = "floorplan-yolo/images"
OUT_LABELS = "floorplan-yolo/labels"
TRAIN_FILE = os.path.join(ROOT, "train.txt")
VAL_FILE = os.path.join(ROOT, "val.txt")
TEST_FILE = os.path.join(ROOT, "test.txt")  # optional, if you have test set

# Make output directories if missing
os.makedirs(OUT_IMAGES, exist_ok=True)
os.makedirs(OUT_LABELS, exist_ok=True)

label_map = {
    'wall': 0,
    'window': 1,
    'door': 2
}

def get_image_size(path):
    with Image.open(path) as img:
        return img.size

def get_bbox(x, y, w, h, img_w, img_h):
    xc = (x + w / 2) / img_w
    yc = (y + h / 2) / img_h
    return [xc, yc, w / img_w, h / img_h]

def polygon_to_bbox(points_str, img_w, img_h):
    try:
        points = []
        for pt in points_str.strip().split():
            coords = pt.strip().split(',')
            if len(coords) != 2:
                continue
            points.append(tuple(map(float, coords)))
        if len(points) < 3:
            # Not a valid polygon
            return None
        xs = [x for x, y in points]
        ys = [y for x, y in points]
        x, y = min(xs), min(ys)
        w, h = max(xs) - x, max(ys) - y
        return get_bbox(x, y, w, h, img_w, img_h)
    except Exception as e:
        print("❌ polygon parsing failed:", e)
        return None

def detect_label(raw_str):
    if not raw_str:
        return None
    raw_str = raw_str.lower()
    if "wall" in raw_str:
        return "wall"
    elif "window" in raw_str:
        return "window"
    elif "door" in raw_str:
        return "door"
    return None

def walk_svg(element, current_label, img_w, img_h, labels):
    cls = element.attrib.get('class', '')
    eid = element.attrib.get('id', '')
    new_label = detect_label(cls) or detect_label(eid) or current_label

    tag = element.tag.split('}')[-1]

    if tag == 'polygon':
        points = element.attrib.get('points')
        if not points:
            return
        bbox = polygon_to_bbox(points, img_w, img_h)
        if bbox and new_label in label_map:
            xc, yc, ww, hh = bbox
            label_line = f"{label_map[new_label]} {xc:.6f} {yc:.6f} {ww:.6f} {hh:.6f}"
            labels.append(label_line)
            print(f"✅ Found {new_label}: {label_line}")

    elif tag == 'rect':
        try:
            x = float(element.attrib['x'])
            y = float(element.attrib['y'])
            w = float(element.attrib['width'])
            h = float(element.attrib['height'])
            bbox = get_bbox(x, y, w, h, img_w, img_h)
            if new_label in label_map:
                xc, yc, ww, hh = bbox
                label_line = f"{label_map[new_label]} {xc:.6f} {yc:.6f} {ww:.6f} {hh:.6f}"
                labels.append(label_line)
                print(f"✅ Found {new_label}: {label_line}")
        except:
            return

    # Recurse into children
    for child in element:
        walk_svg(child, new_label, img_w, img_h, labels)

def parse_svg(svg_file, img_file, output_txt):
    img_w, img_h = get_image_size(img_file)
    try:
        tree = ET.parse(svg_file)
    except ET.ParseError as e:
        print(f"❌ Failed to parse SVG {svg_file}: {e}")
        return False

    root = tree.getroot()
    labels = []

    print(f"\n📂 Parsing {svg_file}")
    walk_svg(root, None, img_w, img_h, labels)

    if labels:
        with open(output_txt, "w") as f:
            f.write("\n".join(labels))
        print(f"💾 Saved labels to {output_txt}")
        return True
    else:
        print("⚠️ No valid labels found")
        return False

def process_file_list(file_list_path, split_name):
    if not os.path.exists(file_list_path):
        print(f"⚠️ {split_name} file not found: {file_list_path}")
        return []

    with open(file_list_path, "r") as f:
        lines = f.read().splitlines()

    print(f"\n🚀 Processing {len(lines)} {split_name} entries from {file_list_path}")

    # Make split directories inside images and labels folders
    split_img_dir = os.path.join(OUT_IMAGES, split_name)
    split_lbl_dir = os.path.join(OUT_LABELS, split_name)
    os.makedirs(split_img_dir, exist_ok=True)
    os.makedirs(split_lbl_dir, exist_ok=True)

    processed_files = []

    for folder_rel_path in lines:
        folder_rel_path = folder_rel_path.strip().strip('/')
        folder_path = os.path.join(ROOT, folder_rel_path)
        img_path = os.path.join(folder_path, "F1_scaled.png")
        svg_path = os.path.join(folder_path, "model.svg")

        if not os.path.exists(img_path) or not os.path.exists(svg_path):
            print(f"❌ Missing image or svg in {folder_path}, skipping...")
            continue

        base_name = folder_rel_path.replace('/', '_') + ".png"
        out_img_path = os.path.join(split_img_dir, base_name)
        out_label_path = os.path.join(split_lbl_dir, folder_rel_path.replace('/', '_') + ".txt")

        # Copy image
        shutil.copy(img_path, out_img_path)

        # Parse and create label file
        parse_svg(svg_path, img_path, out_label_path)

        processed_files.append(base_name)

    print(f"✅ {split_name} processing done: {len(processed_files)} files")
    return processed_files


# === Main ===

train_files = process_file_list(TRAIN_FILE, "train")
val_files = process_file_list(VAL_FILE, "val")
test_files = process_file_list(TEST_FILE, "test") if os.path.exists(TEST_FILE) else []

# Create YAML file for YOLOv8 with correct paths

yaml_content = f"""
path: {os.path.abspath('floorplan-yolo')}
train: images/train
val: images/val
test: images/test  # remove or comment if test set not used
names:
  0: wall
  1: window
  2: door
"""

yaml_path = os.path.join("floorplan-yolo", "data.yaml")
with open(yaml_path, "w") as f:
    f.write(yaml_content.strip())

print(f"\n💾 YOLOv8 data.yaml file saved at {yaml_path}")

