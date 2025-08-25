# -*- coding: utf-8 -*-
"""
build_manifest.py — Tạo manifest.json cho web từ các file link trong thư mục Fall*/
- Quét mọi thư mục bắt đầu bằng 'Fall' (cấp 1) ở thư mục hiện tại
- Tìm các file *_images.txt và *_videos.txt (đệ quy)
- Đọc từng dòng (link), hợp nhất, lọc trùng, ghi vào manifest.json theo tên thư mục

Cách chạy:
  python build_manifest.py
  # Tuỳ chọn:
  # python build_manifest.py --root . --out manifest.json
"""

import os, re, json, argparse
from pathlib import Path

def collect_links_in_dir(folder: Path):
    """Tìm mọi *_images.txt và *_videos.txt trong 'folder' (đệ quy) và trả về list link (không trùng)."""
    links = []
    for p in folder.rglob('*_images.txt'):
        links += read_nonempty_lines(p)
    for p in folder.rglob('*_videos.txt'):
        links += read_nonempty_lines(p)
    # Lọc trùng + bỏ dòng không phải link
    seen = set()
    uniq = []
    for line in links:
        s = line.strip()
        if not s: continue
        if not looks_like_url(s): continue
        if s in seen: continue
        seen.add(s); uniq.append(s)
    return uniq

def read_nonempty_lines(path: Path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [ln.strip() for ln in f if ln.strip()]
    except Exception:
        return []

def looks_like_url(s: str) -> bool:
    return s.startswith('http://') or s.startswith('https://')

def main():
    ap = argparse.ArgumentParser(description="Tạo manifest.json từ các *_images.txt và *_videos.txt trong Fall*/")
    ap.add_argument('--root', default='.', help='Thư mục gốc để quét (mặc định: .)')
    ap.add_argument('--out',  default='manifest.json', help='Đường dẫn file manifest output (mặc định: manifest.json)')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    fall_dirs = [p for p in root.iterdir() if p.is_dir() and p.name.startswith('Fall')]
    fall_dirs.sort(key=lambda p: p.name.lower())

    manifest = {}
    total = 0
    for d in fall_dirs:
        links = collect_links_in_dir(d)
        if not links:
            # không có link nào → bỏ qua danh mục này
            continue
        manifest[d.name] = links
        total += len(links)

    if not manifest:
        print("❌ Không tìm thấy link trong bất kỳ thư mục Fall*/ nào. Hãy chắc rằng đã có các file *_images.txt/_videos.txt.")
        return

    out_path = Path(args.out)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã tạo {out_path} với {len(manifest)} danh mục / {total} link.")

if __name__ == '__main__':
    main()