# -*- coding: utf-8 -*-
"""生成统一的「武者招式」拳谱图（同一武者、统一画风、九式）。
OpenRouter / Gemini Nano Banana。密钥读 /tmp/orkey，不入库。
用法：python3 tools/gen_moves.py        （已存在则跳过，FORCE=1 强制重生）
"""
import os
import time
import base64
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

KEY = open("/tmp/orkey").read().strip()
OUT = os.path.join(os.path.dirname(__file__), "..", ".vitepress", "theme", "assets")
MODEL = "google/gemini-2.5-flash-image"

# 统一的武者 + 画风（每张只换招式，保证成套）
STYLE = (
    "Ancient Chinese martial-arts manual (quanpu) woodblock plate. "
    "ALWAYS the SAME single character: a calm young male martial artist, hair in a neat topknot, "
    "clean-shaven, wearing the SAME simple flowing robe in muted sage-green with sand-beige sash. "
    "Full body, dignified, side or three-quarter view. "
    "Hand-drawn fine ink line-drawing with very light warm ink wash, antique woodblock manual aesthetic, "
    "on warm ivory rice-paper, lots of negative space, elegant and restrained, perfectly consistent "
    "character design and line style across all plates. "
    "NOT photorealistic, NOT 3D, NOT anime, NO color saturation, NO neon, NO modern objects, "
    "NO text, NO numbers, NO seal, NO border frame. One centered figure, minimal background."
)

MOVES = [
    ("m-01", "standing upright in a calm opening stance (qishi), feet together, both arms relaxed and slightly forward"),
    ("m-02", "performing a fist-and-palm salute (baoquan li), one fist wrapped by the other palm at chest"),
    ("m-03", "in a low horse stance (mabu) thrusting one straight punch forward, the other fist chambered at the waist"),
    ("m-04", "pushing both open palms slowly forward at chest height (tui zhang), weight settled"),
    ("m-05", "balancing on one leg in golden-rooster stance (jinji duli), other knee raised, hands poised"),
    ("m-06", "tai-chi 'grasp the sparrow's tail', arms rounded as if holding a large ball, soft and circular"),
    ("m-07", "twisting with both arms parting outward like 'parting the clouds' (bo yun), wide graceful sweep"),
    ("m-08", "standing qigong, both palms cupped at the lower abdomen (dantian), a faint wisp of inner energy"),
    ("m-09", "standing tall, one arm raised overhead with sword-fingers (jian zhi) extended, the other hand low"),
]


def gen(name, pose):
    path = os.path.join(OUT, name + ".png")
    if os.path.exists(path) and os.getenv("FORCE") != "1":
        return name, "skip"
    prompt = f"A martial artist {pose}. {STYLE}"
    for attempt in range(4):
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "X-Title": "neigong-moves"},
                json={"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                      "modalities": ["image", "text"], "image_config": {"aspect_ratio": "1:1"}},
                timeout=180,
            )
            if r.status_code != 200:
                return name, f"HTTP {r.status_code} {r.text[:100]}"
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
    print(f"生成 {len(MOVES)} 式…")
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(gen, n, p): n for n, p in MOVES}
        for f in as_completed(futs):
            n, msg = f.result()
            print(f"  {n}  {msg}")
    print("完成")


if __name__ == "__main__":
    main()
