#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_manifest.py
Quét TẤT CẢ thư mục cấp 1 (mỗi thư mục là 1 danh mục) và tạo manifest.json
liệt kê các file .jpg và .mp4 bên trong (đệ quy các thư mục con).
Cách chạy (tại root repo):
    python make_manifest.py --root "." --output manifest.json
"""

import argparse, json, os
from pathlib import Path

IMG = {'.jpg'}    # đúng yêu cầu: chỉ JPG
VID = {'.mp4'}    # đúng yêu cầu: chỉ MP4
ALL = IMG | VID

# Có thể thêm thư mục muốn bỏ qua ở cấp 1 (nếu cần)
SKIP_TOP = {'.git', '.github', '.well-known'}

def list_media_under(root: Path, top: Path):
    results = []
    for dirpath, dirnames, filenames in os.walk(top):
        dirnames.sort()
        filenames.sort()
        for fn in filenames:
            if fn.startswith('.'):
                continue
            ext = Path(fn).suffix.lower()
            if ext in ALL:
                full = Path(dirpath) / fn
                rel = full.relative_to(root).as_posix()
                results.append(rel)
    return results

def main():
    ap = argparse.ArgumentParser(description='Tạo manifest.json (chỉ .jpg và .mp4) từ các thư mục cấp 1')
    ap.add_argument('--root', type=str, default='.', help='Thư mục gốc repo (chứa index.html)')
    ap.add_argument('--output', type=str, default='manifest.json', help='Tên file manifest xuất ra')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    manifest = {}
    for p in sorted(root.iterdir()):
        if not p.is_dir():
            continue
        name = p.name
        if name.startswith('.') or name in SKIP_TOP:
            continue
        # mỗi thư mục cấp 1 là 1 danh mục
        manifest[name] = list_media_under(root, p)

    out = root / args.output
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✔ Đã tạo {out}")
    for k, v in manifest.items():
        print(f"  {k}: {len(v)} file")

if __name__ == '__main__':
    main()
