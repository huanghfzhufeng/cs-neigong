# -*- coding: utf-8 -*-
"""批量生成成套水墨插画资产（统一画风）。OpenRouter / Gemini Nano Banana。
密钥从 /tmp/orkey 读，不入库。用法：python3 tools/gen_assets.py [组名]
组名：hero | topics | decor | all（默认 all）
"""
import sys
import os
import base64
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

KEY = open("/tmp/orkey").read().strip()
OUT = os.path.join(os.path.dirname(__file__), "..", ".vitepress", "theme", "assets")
os.makedirs(OUT, exist_ok=True)
MODEL = "google/gemini-2.5-flash-image"

# 统一画风（每张都拼这段，保证成套）
STYLE = (
    "Traditional Chinese ink-wash xieyi (freehand) editorial illustration, expressive loose brushwork, "
    "on warm ivory rice-paper. Restrained, elegant, premium, generous negative space, soft paper grain. "
    "Palette ONLY: ivory/cream paper, charcoal ink, terracotta & vermilion accents, muted sage and sand earth tones. "
    "NOT photorealistic, NOT 3D, NOT anime, NOT sci-fi, NO neon, NO blue glow, NO modern objects. "
    "NO text, NO letters, NO numbers, NO watermark, NO seal stamp, NO border. Single clear subject, centered, minimal."
)

HERO = [
    ("hero-a", "1:1", "A lone wuxia martial-arts master seated in deep meditation, robes flowing, a faint thread of inner energy (qi) rising from the dantian, sitting on a simple stone. Bold expressive ink, lots of empty paper."),
    ("hero-b", "1:1", "A martial-arts cultivator in a slow standing qigong pose, one palm raised, a ribbon of qi swirling around the body, very freehand xieyi ink, atmospheric, large negative space."),
    ("hero-c", "4:3", "A small lone cultivator seated in meditation on a cliff above a sea of clouds, distant ink mountains, vast empty sky, minimalist atmospheric shan-shui ink painting."),
    ("hero-d", "1:1", "Side profile of a seated cultivator meditating, a single bold sweeping ink brushstroke forms the ground beneath, a thin vermilion line of qi rising, very minimal xieyi."),
]

TOPICS = [
    ("t-01", "an old wooden abacus (suanpan) with beads, resting on a low table"),                # 计组
    ("t-02", "a set of interlocking mechanical gears and a small hourglass, a coordinating mechanism"),  # 操作系统
    ("t-03", "two carrier pigeons in flight between two distant mountain pavilions, a faint connecting thread"),  # 网络
    ("t-04", "a single elegant tree with clearly branching limbs (like a data tree), a few leaves"),  # 数据结构与算法
    ("t-05", "a tall ancient wooden bookshelf filled with neatly rolled scrolls, an archive pavilion"),  # MySQL
    ("t-06", "a multi-tier pagoda rising taller with light bamboo scaffolding, growing architecture"),  # 架构演进
    ("t-07", "a traditional hanging balance scale weighing two stones of different size, equilibrium"),  # 质量属性/评估
    ("t-08", "a carpenter's ink-marker (mo-dou) with an L-shaped try-square and a rolled blueprint"),  # 软件工程
    ("t-09", "a calligraphy master guiding a single floating brush that writes by itself, a wisp of spirit energy"),  # LLM/Agent
]

DECOR = [
    ("d-mountains", "16:9", "A wide minimalist shan-shui ink landscape: layered distant mountains fading into mist, vast empty warm-ivory sky, a few faint trees. Atmospheric, lots of empty space, banner composition."),
    ("d-clouds", "16:9", "Elegant stylized auspicious cloud patterns (xiangyun) painted in soft ink with faint terracotta tint, drifting across warm ivory paper, decorative band, minimal."),
    ("d-brush", "16:9", "A single bold horizontal sumi-e brush sweep in charcoal ink with a dry-brush tapered end and a touch of vermilion, on warm ivory paper, lots of empty space."),
]


import time

def gen(name, aspect, subject):
    path = os.path.join(OUT, name + ".png")
    if os.path.exists(path) and os.getenv("FORCE") != "1":
        return name, "skip(已存在)"
    prompt = f"{subject}. {STYLE}"
    for attempt in range(4):
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "X-Title": "neigong-assets"},
                json={"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                      "modalities": ["image", "text"], "image_config": {"aspect_ratio": aspect}},
                timeout=180,
            )
            if r.status_code != 200:
                return name, f"HTTP {r.status_code} {r.text[:120]}"
            imgs = r.json()["choices"][0]["message"].get("images") or []
            if not imgs:
                return name, "no image"
            b = base64.b64decode(imgs[0]["image_url"]["url"].split(",", 1)[1])
            open(path, "wb").write(b)
            return name, f"OK {len(b)//1024}KB"
        except Exception as e:
            if attempt == 3:
                return name, f"ERR {e}"
            time.sleep(3 + attempt * 3)


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    jobs = []
    if which in ("hero", "all"):
        jobs += [(n, a, p) for n, a, p in HERO]
    if which in ("topics", "all"):
        jobs += [(n, "1:1", p) for n, p in TOPICS]
    if which in ("decor", "all"):
        jobs += [(n, a, p) for n, a, p in DECOR]
    print(f"生成 {len(jobs)} 张…")
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(gen, n, a, p): n for n, a, p in jobs}
        for f in as_completed(futs):
            n, msg = f.result()
            print(f"  {n:14} {msg}")
    print("完成")


if __name__ == "__main__":
    main()
