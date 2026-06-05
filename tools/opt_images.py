# -*- coding: utf-8 -*-
"""把生成的 PNG 资产压成按显示尺寸缩小的 WebP，大幅减小首页体积。
PNG 原图保留在本地但不入库（.gitignore），站点只用 webp。"""
import os
import glob
from PIL import Image

A = os.path.join(os.path.dirname(__file__), "..", ".vitepress", "theme", "assets")
WIDTH = {
    "hero-cultivator": 760, "hero-a": 760, "hero-b": 760, "hero-c": 1000, "hero-d": 760,
    "d-mountains": 1280, "d-clouds": 1200, "d-brush": 720,
}
DEFAULT = 560  # 主题图：既当 ~120px 印记又当 ~360px 卡片，560 足够清晰

total = 0
for p in sorted(glob.glob(os.path.join(A, "*.png"))):
    name = os.path.splitext(os.path.basename(p))[0]
    im = Image.open(p).convert("RGB")
    tw = WIDTH.get(name, DEFAULT)
    if im.width > tw:
        im = im.resize((tw, round(im.height * tw / im.width)), Image.LANCZOS)
    out = os.path.join(A, name + ".webp")
    im.save(out, "WEBP", quality=82, method=6)
    kb = os.path.getsize(out) // 1024
    total += kb
    print(f"  {name:16} {im.size}  {kb} KB")
print(f"合计 webp ≈ {total} KB")
