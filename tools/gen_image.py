# -*- coding: utf-8 -*-
"""用 OpenRouter 的图像模型（Gemini Nano Banana）生成插画资产。

用法：echo "<prompt>" | python3 tools/gen_image.py <out.png> [aspect] [model]
  aspect 默认 1:1；model 默认 google/gemini-2.5-flash-image
密钥从 /tmp/orkey 读取（不写进代码、不进 git）。
"""
import sys
import base64
import json
import requests

KEY = open("/tmp/orkey").read().strip()
out = sys.argv[1]
aspect = sys.argv[2] if len(sys.argv) > 2 else "1:1"
model = sys.argv[3] if len(sys.argv) > 3 else "google/gemini-2.5-flash-image"
prompt = sys.stdin.read().strip()

resp = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "X-Title": "neigong-assets",
    },
    json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": aspect},
    },
    timeout=180,
)

if resp.status_code != 200:
    print("HTTP", resp.status_code, resp.text[:600])
    sys.exit(1)

data = resp.json()
msg = data["choices"][0]["message"]
imgs = msg.get("images") or []
if not imgs:
    print("无图片返回。message keys:", list(msg.keys()))
    print("content:", str(msg.get("content"))[:300])
    sys.exit(2)

url = imgs[0]["image_url"]["url"]
b64 = url.split(",", 1)[1]
with open(out, "wb") as f:
    f.write(base64.b64decode(b64))
print(f"OK 生成 {out}  模型 {model}  比例 {aspect}  字节 {len(base64.b64decode(b64))}")
