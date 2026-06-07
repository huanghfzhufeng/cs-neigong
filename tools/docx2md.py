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
    # 去软考/案例分析应试框架（架构风格与设计这门），保留技术内容
    ("这是案例分析和论文的承重块,也是你架构师知识里最后一块大的缺口。", ""),
    ("案例常常给一个场景,让你选合适的架构风格,并说明它如何支撑所需的质量属性。",
     "给定一个场景,你能选出合适的风格,并说清它如何支撑所需的质量。"),
    ("这块是案例的黄金搭档。案例常考", "它和质量属性是黄金搭档"),
    ("论文常考「论软件架构风格」「论某类系统的架构设计」。", ""),
    ("再用历年真题练「给场景选风格 + 论证」", "再找真实场景练「给场景选风格 + 讲理由」"),
    ("案例两大核心", "系统设计的两大支柱"),
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
    # 转义“像 HTML 标签”的 <（如 <script>、<html>），否则 VitePress(Vue) 会当成标签解析报错
    s = re.sub(r"<(?=[A-Za-z/!?])", "&lt;", s)
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


DROP_RE = re.compile(r"^怎么用这份资料")
# 各文档方框标签家族 → 统一重构标签。
# 从具体到一般匹配；消费可选的括号注（如“(背这段)”“(讲清就够)”）和分隔符。
LABEL_RULES = [
    (re.compile(r"^(?:面试这样答|面试速答|核心要点|核心)(?:\s*[（(][^）)]*[）)])?\s*[:：]?\s*"),
     "一句话讲透", "quote"),
    (re.compile(r"^(?:面试前最后叮嘱|给你的叮嘱)\s*[:：]?\s*"),
     "抓住这几点", "points"),
    (re.compile(r"^复习建议\s*[:：]?\s*"),
     "学习建议", "section"),
    (re.compile(r"^(?:经典题\s*/?\s*高频追问|高频追问(?:\s*/?\s*延伸)?|经典题|实战(?:\s*/?\s*进阶)?|延伸)\s*[:：]?\s*"),
     "再往下挖", "section"),
    (re.compile(r"^(?:易错点(?:\s*·?\s*别答错)?|坑(?:\s*/?\s*注意)?)\s*[:：]?\s*"),
     "常见误区", "section"),
]


def render_block(label, style, body):
    body = (body or "").strip()
    if not body and not label:
        return None
    if style == "quote":
        line = re.sub(r"\s+", " ", body.replace("\n", " ")).strip()
        return f"> **{label}**\n> {line}" if label else f"> {line}"
    if style == "points":
        items = split_numbered(body) or [body]
        return f"**{label}**\n\n" + "\n".join(f"- {x}" for x in items)
    # section：有 bullet 拆列表，否则散文
    if "•" in body or "▸" in body:
        items = split_bullets(body)
        return f"**{label}**\n\n" + "\n".join(f"- {x}" for x in items)
    return f"**{label}**\n\n{body}"


def reframe_text(raw):
    """把一段方框/合并单元格文本重构成规范 md；元说明返回 None。"""
    full = tidy(raw)
    if not full or DROP_RE.match(full):
        return None
    for rx, label, style in LABEL_RULES:
        m = rx.match(full)
        if m:
            return render_block(label, style, full[m.end():])
    # 叙事框（如“本阶段小结”“Anthropic 的实践”）：首行若像标题就加粗，正文一并收进引用
    head, _, rest = full.partition("\n")
    head = head.strip()
    rest = re.sub(r"\s+", " ", rest.replace("\n", " ")).strip()
    if rest and len(head) <= 16 and not re.search(r"[。！？，,；;]", head):
        return f"> **{head}**\n> {rest}"
    return "> " + re.sub(r"\s+", " ", full.replace("\n", " ")).strip()


def render_callout(cell):
    return reframe_text(cell.text)


def render_table(tbl):
    def cellmd(c):
        t = strip_emoji(c.text).replace(" ", " ").strip()
        t = re.sub(r"<(?=[A-Za-z/!?])", "&lt;", t)  # 先转义标签型 <，再注入 <br>
        t = re.sub(r"\s*\n\s*", "<br>", t)
        t = t.replace("|", "\\|")
        return re.sub(r"[ \t]{2,}", " ", t)

    rows = tbl.rows
    if not rows:
        return ""
    ncol = len(rows[0].cells)

    data, notes = [], []
    for ri, r in enumerate(rows):
        cells = list(r.cells)[:ncol]
        vals = [c.text.strip() for c in cells]
        # 整行横向合并（所有单元格同文且非空）：当作表后旁注，避免重复 N 列
        if ri > 0 and len(set(vals)) == 1 and vals[0]:
            notes.append(cells[0].text)
        else:
            data.append(cells)

    def row_md(cells):
        md = [cellmd(c) for c in cells][:ncol]
        md += [""] * (ncol - len(md))
        return "| " + " | ".join(md) + " |"

    out = [row_md(data[0]), "| " + " | ".join(["---"] * ncol) + " |"]
    out += [row_md(r) for r in data[1:]]
    blocks = ["\n".join(out)]
    for n in notes:                     # 合并行按方框规则重构（多为“高频追问”等）
        b = reframe_text(n)
        if b:
            blocks.append(b)
    return "\n\n".join(blocks)


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
            if len(tbl.columns) == 1:
                # 单列表格一律是提示框（可能多行），合并各行文本后重构
                text = "\n".join(c.text for r in tbl.rows for c in r.cells)
                blk = reframe_text(text)
                if blk:
                    blocks.append(blk)
            else:
                blk = render_table(tbl)
                if blk:
                    blocks.append(blk)
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
    # 第二个 ## 标题 = 第一个正式章节（第一个是引言）。vibe 段放它之前 → 即引言之后。
    heads = [i for i, b in enumerate(blocks)
             if isinstance(b, str) and b.startswith("## ")]
    vibe_at = heads[1] if len(heads) >= 2 else len(blocks)

    md = [f"# {cover_title or slug}", "<!-- LEAD -->"]  # LEAD 由注入脚本填一句话导言
    for i, b in enumerate(blocks):
        if i == vibe_at:
            md.append("<!-- VIBE-INTRO -->")  # 人工补「把它用在 vibe coding 上」
        if isinstance(b, list):
            md.append(f"![{b[2]}]({b[1]})")
        elif is_label(b):
            md.append(f"**{b}**")
        else:
            md.append(b)
    if vibe_at >= len(blocks):
        md.append("<!-- VIBE-INTRO -->")

    out = "\n\n".join(md) + "\n"
    out = re.sub(r"\n{3,}", "\n\n", out)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"OK  {out_path}  ({len(blocks)} blocks, {len(saved)} images)")


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2], sys.argv[3])
