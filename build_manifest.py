# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

SRC = Path("manifest.json")
DST = Path("manifest.json")  # ghi đè

def is_image(u):
    return bool(re.search(r'\.(jpg|jpeg|png|webp|gif|bmp|heic|heif|tif|tiff)(\?|$)', u, re.I)) \
           or 'drive.google.com/uc?id=' in u

def is_video(u):
    return bool(re.search(r'\.(mp4|webm|mkv|mov|avi|3gp|m3u8|ts)(\?|$)', u, re.I)) \
           or 'drive.google.com/file/' in u

data = json.loads(SRC.read_text(encoding="utf-8"))
out = {}
for cat, arr in data.items():
    if not isinstance(arr, list):  # đã đúng dạng mới
        out[cat] = arr
        continue
    imgs, vids = [], []
    for u in arr:
        if is_image(u): imgs.append(u)
        elif is_video(u): vids.append(u)
    if imgs or vids:
        out[cat] = {"images": imgs, "videos": vids}

DST.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ Converted → {DST} (categories: {len(out)})")