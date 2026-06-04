#!/usr/bin/env python3
"""把「面试图文详解」系列 docx 转成规范、无 AI 味的 Markdown。

设计目标（一把尺子量 10 份）：
- 保留原文措辞与配图（内容扎实，不重写）。
- 去掉一切装饰性 emoji（📌🎯💡⚠ 等）和应试外壳。
- 把方框重贴成求知导向标签：一句话讲透 / 再往下挖 / 常见误区。
- 真表格转标准 Markdown 表格；▸ 列表转 - 列表。
- vibe coding 视角由人工逐篇补写（本脚本不臆造内容）。

用法: docx2md.py <input.docx> <output.md> <slug>
配图输出到 <output 所在目录>/assets/<slug>/
"""
import sys, os, re
import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.table import Table

# --- 装饰性 emoji / 变体选择符（不动 ▸ U+25B8 和 • U+2022，它们当列表标记处理）---
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿⬀-⯿️←-⇿⌀-⏿]"
)
# 应试话术清洗（仅去壳，不改技术正文表达）
DECRAM = [
    ("(背这段)", ""), ("（背这段）", ""), ("· 别答错", ""), ("·别答错", ""),
    ("别答错", ""), ("绿框速答", "“一句话讲透”"), ("绿框", "“一句话讲透”"),
    ("背熟", "讲清楚"), ("拿分", "答好"), ("面试叮嘱", "要点回顾"),
    # 只清“落款”式应试措辞，正文其余“面试/八股”照原文保留
    ("祝面试顺利", "愿你真正把它用起来"), ("面试重灾区", "重难点"),
    ("祝你拿下心仪的 offer", "愿你把它真正用起来"),
    ("祝你拿下心仪的offer", "愿你把它真正用起来"),
]
CAPTION_RE = re.compile(r"^图\s*[0-9０-９]")


def is_label(s):
    """短标签行（表格/列表前的小标题），加粗以免成为孤儿段落。"""
    if not s or s[0] in "#|>-*!<" or "\n" in s:
        return False
    if re.search(r"[。！？]", s) or s.endswith(("，", ",", "、", "；", ";", "：", ":")):
        return False
    return len(s) <= 26


def strip_emoji(s):
    return EMOJI.sub("", s or "")


def tidy(s):
    s = strip_emoji(s).replace(" ", " ")
    for a, b in DECRAM:
        s = s.replace(a, b)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()


def split_bullets(text):
    """按 • ▸ 拆成条目；首段非空则作为引导句返回。"""
    parts = re.split(r"\s*[•▸]\s*", text)
    parts = [p.strip(" :：") for p in parts if p.strip(" :：")]
    return parts


def split_numbered(text):
    parts = re.split(r"\s*\d+[)）]\s*", text)
    return [p.strip(" :：;；") for p in parts if p.strip(" :：;；")]


def bold_term(item):
    """术语 —— 说明  →  **术语** —— 说明"""
    m = re.match(r"(.{1,18}?)\s*——\s*(.+)", item)
    if m:
        return f"**{m.group(1).strip()}** —— {m.group(2).strip()}"
    return item


def render_callout(cell):
    full = tidy(cell.text)
    if not full:
        return None
    if full.startswith("怎么用这份资料"):
        return None  # 元说明并入 README

    label, style, body = None, "quote", full
    rules = [
        (("面试这样答", "面试速答"), "一句话讲透", "quote"),
        (("面试前最后叮嘱",), "抓住这几点", "points"),
        (("高频追问 / 延伸", "高频追问/延伸", "高频追问", "延伸"), "再往下挖", "section"),
        (("易错点",), "常见误区", "section"),
    ]
    for prefixes, lab, sty in rules:
        for ph in prefixes:
            if full.startswith(ph):
                body = full[len(ph):].strip().strip(" :：·—-/").strip()
                label, style = lab, sty
                break
        if label:
            break

    body = body.strip()
    if style == "quote":
        line = re.sub(r"\s+", " ", body.replace("\n", " ")).strip()
        return (f"> **{label}**\n> {line}" if label else f"> {line}")
    if style == "points":
        items = split_numbered(body) or [body]
        return f"**{label}**\n\n" + "\n".join(f"- {x}" for x in items)
    # section: 有 bullet 拆列表，否则散文
    if "•" in body or "▸" in body:
        items = split_bullets(body)
        return f"**{label}**\n\n" + "\n".join(f"- {x}" for x in items)
    return f"**{label}**\n\n{body}"


def render_table(tbl):
    def cellmd(c):
        t = strip_emoji(c.text).replace(" ", " ").strip()
        t = re.sub(r"\s*\n\s*", "<br>", t)
        t = t.replace("|", "\\|")
        return re.sub(r"[ \t]{2,}", " ", t)

    rows = tbl.rows
    if not rows:
        return ""
    ncol = len(rows[0].cells)
    def fix(cells):
        cells = list(cells)[:ncol]
        cells += [""] * (ncol - len(cells))
        return cells
    out = ["| " + " | ".join(cellmd(c) for c in fix(rows[0].cells)) + " |"]
    out.append("| " + " | ".join(["---"] * ncol) + " |")
    for r in rows[1:]:
        out.append("| " + " | ".join(cellmd(c) for c in fix(r.cells)) + " |")
    return "\n".join(out)


def convert(in_path, out_path, slug):
    d = docx.Document(in_path)
    assets_dir = os.path.join(os.path.dirname(out_path), "assets", slug)
    os.makedirs(assets_dir, exist_ok=True)

    saved = {}
    def save_image(rid):
        if rid in saved:
            return saved[rid]
        part = d.part.related_parts[rid]
        ext = os.path.splitext(part.partname)[1] or ".png"
        fn = f"img-{len(saved) + 1:02d}{ext}"
        with open(os.path.join(assets_dir, fn), "wb") as f:
            f.write(part.blob)
        rel = f"assets/{slug}/{fn}"
        saved[rid] = rel
        return rel

    def img_rids(el):
        return [b.get(qn("r:embed")) for b in el.findall(".//" + qn("a:blip"))
                if b.get(qn("r:embed"))]

    blocks = []            # str 或 ["IMG", relpath, alt]
    bullet_buf = []
    def flush():
        if bullet_buf:
            blocks.append("\n".join(bullet_buf))
            bullet_buf.clear()

    seen_heading = False
    cover_title = None
    cover_scope = None

    for child in d.element.body.iterchildren():
        tag = child.tag.split("}")[-1]

        if tag == "tbl":
            if not seen_heading:
                continue  # 封面区若有表格，忽略
            flush()
            tbl = Table(child, d)
            if len(tbl.rows) == 1 and len(tbl.columns) == 1:
                blk = render_callout(tbl.cell(0, 0))
                if blk:
                    blocks.append(blk)
            else:
                blocks.append(render_table(tbl))
            continue

        if tag != "p":
            continue
        p = Paragraph(child, d)
        text = tidy(p.text)
        rids = img_rids(child)
        is_heading = bool(p.style and p.style.name == "Heading 1")

        # --- 封面区：取标题与“覆盖”行，丢弃应试口号与目录 ---
        if not seen_heading and not is_heading:
            if text and cover_title is None:
                cover_title = text
            elif text.startswith("覆盖"):
                cover_scope = text
            continue

        if is_heading:
            seen_heading = True
            flush()
            blocks.append("## " + text)
            continue

        if rids:                         # 图片段落
            flush()
            for rid in rids:
                blocks.append(["IMG", save_image(rid), ""])
            continue

        if CAPTION_RE.match(text) and blocks and isinstance(blocks[-1], list) \
                and blocks[-1][2] == "":
            blocks[-1][2] = text         # 给上一张图补题注
            continue

        if not text:
            continue

        if text.startswith("▸"):         # 正文 ▸ 列表项
            bullet_buf.append("- " + bold_term(text[1:].strip()))
            continue

        flush()
        blocks.append(text)              # 普通段落

    flush()

    # --- 组装 ---
    md = [f"# {cover_title or slug}"]
    if cover_scope:
        scope = cover_scope.split("覆盖", 1)[-1].lstrip(":：").strip()
        md.append(f"**覆盖**：{scope}")
    md.append("<!-- VIBE-INTRO -->")   # 人工补「把它用在 vibe coding 上」
    for b in blocks:
        if isinstance(b, list):
            md.append(f"![{b[2]}]({b[1]})")
        elif is_label(b):
            md.append(f"**{b}**")
        else:
            md.append(b)

    out = "\n\n".join(md) + "\n"
    out = re.sub(r"\n{3,}", "\n\n", out)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"OK  {out_path}  ({len(blocks)} blocks, {len(saved)} images)")


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2], sys.argv[3])
