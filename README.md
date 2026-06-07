# 内功

**在线阅读 → https://huanghfzhufeng.github.io/cs-neigong/**

> 招式人人会，内功定高下。
>
> vibe coding 时代，模型什么都能做——做得好不好，看你的内功有多深。这套手册把计算机底层一份份讲透：是什么、为什么、解决什么、怎么用。懂了底层，你才压得住模型，而不是把垃圾越堆越高。人和模型相互成就，你的上限，决定它能帮你到哪。

## 内容（持续增加）

按内功的层次铺开：

- **地基**：计算机组成原理 · 数据结构与算法
- **运行与连接**：操作系统 · 计算机网络
- **数据与架构**：MySQL · 互联网架构演进
- **方法与上层**：系统质量属性与架构评估 · 软件工程 · 架构风格与设计 · LLM 与 Agent 工程

每章的结构：**一句话讲透**（是什么）→ 展开为什么 + 配图 →**再往下挖**→**常见误区**→**放到 vibe coding 里**（怎么判断模型给的对不对）。

## 本地开发 / 重新生成

`.md` 视作构建产物：源 `.docx` → 脚本生成 → VitePress 构建。

```bash
# 1) docx → 扁平 md（含配图）
python3 tools/docx2md.py <源.docx> <NN-名称.md> <NN-名称>
# 2) 注入「放到 vibe coding 里」等视角（可复现，改文案就改这个脚本）
python3 tools/inject_vibe.py
# 3) 拆成逐章页 + 生成侧栏/导航（hello-algo 式结构）
python3 tools/split_build.py
# 4) 本地预览 / 构建
npm install
npm run docs:dev      # http://localhost:5173/cs-neigong/
npm run docs:build
```

**加新一份**：在 `tools/split_build.py` 的 `TOPICS` 加一行、`.vitepress/theme/Landing.vue` 的 `DESC` 补一句描述，跑一遍第 2→3 步即可——侧栏、顶部导航、首页卡片都会自动归位，不锁死份数。

推送到 `main` 分支即由 GitHub Actions 自动构建并部署到 GitHub Pages。
