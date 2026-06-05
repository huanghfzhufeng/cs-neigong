# -*- coding: utf-8 -*-
"""把 9 份扁平 md 拆成 hello-algo 式结构：每个主题一个文件夹，每章一页。

输入：根目录的 NN-主题.md（docx2md + inject_vibe 生成）+ assets/NN-主题/ 配图。
输出：
  NN-主题/index.md        —— 概览（导言 + 引言 + 把它用在 vibe coding 上 + 本篇章节）
  NN-主题/chNN.md          —— 每章一页
  NN-主题/assets/          —— 该主题配图（从 assets/NN-主题/ 移入）
  .vitepress/sidebars.json —— 按主题作用域的侧栏 + 顶部分组导航（单一事实来源）

设计意图：拆页后侧栏只显示当前主题的章节（像 hello-algo）；顶部按 4 大主题分组切换；
新增一份只需在 TOPICS 里加一行，重跑即可——不锁死份数。
"""
import os
import re
import json
import shutil

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

# (slug, 显示名, 所属组)；以后加新份就在这里加一行
TOPICS = [
    ("01-计算机组成原理", "计算机组成原理", "地基"),
    ("02-操作系统", "操作系统", "运行与连接"),
    ("03-计算机网络", "计算机网络", "运行与连接"),
    ("04-数据结构与算法", "数据结构与算法", "地基"),
    ("05-MySQL", "MySQL", "数据与架构"),
    ("06-互联网架构演进", "互联网架构演进", "数据与架构"),
    ("07-系统质量属性与架构评估", "系统质量属性与架构评估", "方法与上层"),
    ("08-软件工程", "软件工程", "方法与上层"),
    ("09-LLM与Agent工程", "LLM 与 Agent 工程", "方法与上层"),
]
GROUP_ORDER = ["地基", "运行与连接", "数据与架构", "方法与上层"]

CHAP = re.compile(r"^## (第\s*[0-9０-９]+\s*章.*)$")


def split_topic(slug: str, name: str):
    flat = f"{slug}.md"
    s = open(flat, encoding="utf-8").read()
    s = s.replace(f"](assets/{slug}/", "](assets/")  # 图片改为主题内相对路径

    os.makedirs(slug, exist_ok=True)
    src, dst = os.path.join("assets", slug), os.path.join(slug, "assets")
    if os.path.isdir(src):
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.move(src, dst)

    lines = s.split("\n")
    title = lines[0].lstrip("# ").strip()
    idxs = [i for i, l in enumerate(lines) if CHAP.match(l)]
    front = "\n".join(lines[1:idxs[0]]).strip() if idxs else "\n".join(lines[1:]).strip()

    items = [{"text": "导言", "link": f"/{slug}/"}]
    chlist = []
    for k, start in enumerate(idxs):
        end = idxs[k + 1] if k + 1 < len(idxs) else len(lines)
        head = CHAP.match(lines[start]).group(1).strip()
        body = "\n".join(lines[start + 1:end]).strip()
        fn = f"ch{k + 1:02d}"
        open(os.path.join(slug, fn + ".md"), "w", encoding="utf-8").write(f"# {head}\n\n{body}\n")
        items.append({"text": head, "link": f"/{slug}/{fn}"})
        chlist.append(f"- [{head}](./{fn})")

    index_md = f"# {title}\n\n{front}\n\n## 本篇章节\n\n" + "\n".join(chlist) + "\n"
    open(os.path.join(slug, "index.md"), "w", encoding="utf-8").write(index_md)
    os.remove(flat)
    return {"text": name, "items": items}


def main():
    sidebars = {}
    nav_groups = {g: [] for g in GROUP_ORDER}
    overview = []

    for slug, name, group in TOPICS:
        sb = split_topic(slug, name)
        sidebars[f"/{slug}/"] = [sb]
        nav_groups[group].append({"text": f"{slug[:2]} · {name}", "link": f"/{slug}/"})

    # 全局（导读等）侧栏：4 大主题分组总览，可折叠
    for g in GROUP_ORDER:
        overview.append({"text": g, "collapsed": False, "items": nav_groups[g]})
    sidebars["/"] = overview

    nav = [{"text": "导读", "link": "/00-导读"}]
    for g in GROUP_ORDER:
        nav.append({"text": g, "items": nav_groups[g]})

    os.makedirs(".vitepress", exist_ok=True)
    with open(".vitepress/sidebars.json", "w", encoding="utf-8") as f:
        json.dump({"sidebars": sidebars, "nav": nav}, f, ensure_ascii=False, indent=2)

    pages = sum(len(v[0]["items"]) for k, v in sidebars.items() if k != "/")
    print(f"拆页完成：{len(TOPICS)} 个主题，{pages} 个章页（含概览）")


if __name__ == "__main__":
    main()
