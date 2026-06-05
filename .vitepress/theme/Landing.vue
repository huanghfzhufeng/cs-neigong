<script setup lang="ts">
import { withBase } from 'vitepress'
import { onMounted, onUnmounted } from 'vue'
import site from '../sidebars.json'

const GH = 'https://github.com/huanghfzhufeng/cs-neigong'

function scrollDown() {
  document.querySelector('.below')?.scrollIntoView({ behavior: 'smooth' })
}

// 首页隐藏默认导航，做沉浸式扉页
onMounted(() => document.documentElement.classList.add('home-hero'))
onUnmounted(() => document.documentElement.classList.remove('home-hero'))

// ---------- 目录：从 sidebars.json 自动构建（加新份自动出现）----------
const DESC: Record<string, string> = {
  '01-计算机组成原理': '机器到底怎么算：CPU、cache、内存、总线',
  '02-操作系统': '硬件与应用之间的资源管理者：进程、内存、I/O',
  '03-计算机网络': '数据怎么跨机器送达：TCP/IP、HTTP、HTTPS',
  '04-数据结构与算法': '数据怎么存、问题怎么高效解',
  '05-MySQL': '索引、事务、锁、日志——数据怎么可靠存取',
  '06-互联网架构演进': '从单机到分布式，一步步扛住流量',
  '07-系统质量属性与架构评估': '用“质量属性”的语言谈架构与权衡',
  '08-软件工程': '把事做对、做稳的方法论',
  '09-LLM与Agent工程': '怎么用模型把活干好——元能力',
}
const GROUP_DESC: Record<string, string> = {
  '地基': '机器与数据怎么运转——其余一切的底层支撑',
  '运行与连接': '程序怎么跑、请求怎么到',
  '数据与架构': '怎么可靠存取、怎么扛住流量',
  '方法与上层': '怎么把事做对、怎么用好模型',
}
const groups = (site.nav as any[])
  .filter((n) => Array.isArray(n.items))
  .map((g) => ({
    title: g.text as string,
    desc: GROUP_DESC[g.text] ?? '',
    items: (g.items as any[]).map((it) => {
      const [no, title] = (it.text as string).split(' · ')
      const slug = (it.link as string).replace(/\//g, '')
      return { no, title: title ?? it.text, desc: DESC[slug] ?? '', link: it.link as string }
    }),
  }))
</script>

<template>
  <div class="landing">
    <!-- ===== 秘籍扉页（暖纸 · 全屏 · 入场动效） ===== -->
    <section class="codex">
      <div class="grain"></div>
      <div class="watermark">功</div>

      <header class="cx-top">
        <span class="wordmark">内功</span>
        <a class="gh" :href="GH" target="_blank" rel="noreferrer">GitHub</a>
      </header>

      <div class="cover">
        <p class="kicker rise" style="--d: 0.05s">内功心法 · 计算机底层图文详解</p>

        <div class="title-wrap">
          <h1 class="title rise" style="--d: 0.18s">内功</h1>
          <svg class="brush" viewBox="0 0 320 26" preserveAspectRatio="none" aria-hidden="true">
            <path d="M6 16 C 70 7, 150 21, 220 12 S 300 9, 314 15" />
          </svg>
          <div class="seal" aria-hidden="true"><span>内</span><span>功</span></div>
        </div>

        <p class="epigraph rise" style="--d: 0.42s">招式人人会，内功定高下。</p>
        <p class="sub rise" style="--d: 0.56s">
          vibe coding 时代，模型什么都能做——做得好不好，看你的内功有多深。
        </p>

        <div class="actions rise" style="--d: 0.7s">
          <a class="btn primary" :href="withBase('/00-导读')">开始修炼</a>
          <a class="btn ghost" :href="GH" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </div>

      <button class="scroll-cue rise" style="--d: 1.2s" @click="scrollDown">翻开目录 ↓</button>
    </section>

    <!-- ===== 目录（暖色） ===== -->
    <div class="below">
      <section class="hook">
        <h2>九份，不是九本互不相干的册子</h2>
        <p class="hook-lead">在浏览器敲下回车、到看见页面，这一瞬数据穿过了大半套心法：</p>
        <div class="chain">
          <span class="node">计算机网络</span><i class="arrow">→</i>
          <span class="node">操作系统</span><i class="arrow">→</i>
          <span class="node">互联网架构</span><i class="arrow">→</i>
          <span class="node">MySQL</span>
        </div>
        <p class="hook-foot">
          底下垫着 <b>数据结构</b> 与 <b>计算机组成原理</b>。<a :href="withBase('/00-导读')">看这条脉络怎么贯通 →</a>
        </p>
      </section>

      <section class="catalog">
        <p class="catalog-intro">循序修炼，按内功的层次铺开（持续增加）：</p>
        <div v-for="g in groups" :key="g.title" class="group">
          <div class="group-head">
            <h3>{{ g.title }}</h3>
            <span class="group-desc">{{ g.desc }}</span>
          </div>
          <div class="cards">
            <a v-for="c in g.items" :key="c.no" class="card" :href="withBase(c.link)">
              <span class="no">{{ c.no }}</span>
              <span class="ct">{{ c.title }}</span>
              <span class="cd">{{ c.desc }}</span>
            </a>
          </div>
        </div>
      </section>

      <section class="howto">
        <h2>怎么修炼这套</h2>
        <div class="hcols">
          <div class="hcol"><h4>通读</h4><p>第一遍按顺序读，重点是每个“为什么”和每张图。</p></div>
          <div class="hcol"><h4>速查</h4><p>写代码时冒出疑问，搜索（⌘K）秒级翻到那一页。</p></div>
          <div class="hcol"><h4>炼内功</h4><p>每章末「放到 vibe coding 里」把知识连到“怎么判断模型给的对不对”。</p></div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
/* ===================== 秘籍扉页 ===================== */
.codex {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(130% 110% at 50% -10%, #faf6ec 0%, #f4ede0 58%, #ebe1d0 100%);
}
/* 纸纹 */
.grain {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.5;
  mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.06'/%3E%3C/svg%3E");
}
/* 巨大“功”字水印 */
.watermark {
  position: absolute;
  right: -3vmin;
  bottom: -14vmin;
  font-family: var(--cd-serif);
  font-weight: 600;
  font-size: 56vmin;
  line-height: 1;
  color: #3a2e22;
  opacity: 0.04;
  pointer-events: none;
  user-select: none;
}

.cx-top {
  position: absolute;
  top: 24px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 36px;
  z-index: 5;
}
.wordmark {
  font-family: var(--cd-serif);
  font-size: 1.3rem;
  font-weight: 600;
  color: #2a2620;
  letter-spacing: 0.06em;
}
.gh { color: #6b6053; font-size: 0.9rem; font-weight: 500; }
.gh:hover { color: #2a2620; }

.cover {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 0 24px;
  max-width: 40em;
}
.kicker {
  margin: 0 0 26px;
  color: #b1542f;
  font-size: 0.84rem;
  font-weight: 600;
  letter-spacing: 0.22em;
}
.title-wrap { position: relative; display: inline-block; }
.title {
  margin: 0;
  font-family: var(--cd-serif);
  font-weight: 600;
  font-size: clamp(5rem, 17vw, 10rem);
  line-height: 0.95;
  letter-spacing: 0.05em;
  color: #2a241d;
}
.brush {
  display: block;
  width: 100%;
  height: 22px;
  margin: 6px auto 0;
  overflow: visible;
}
.brush path {
  fill: none;
  stroke: #c2603f;
  stroke-width: 9;
  stroke-linecap: round;
  stroke-dasharray: 360;
  stroke-dashoffset: 360;
  animation: draw 0.9s cubic-bezier(0.65, 0, 0.35, 1) forwards;
  animation-delay: 0.62s;
}
@keyframes draw { to { stroke-dashoffset: 0; } }

/* 朱红印章（白文「内功」），落款式盖章 */
.seal {
  position: absolute;
  top: -6%;
  right: -86px;
  width: clamp(58px, 7.6vw, 84px);
  height: clamp(58px, 7.6vw, 84px);
  background: #b5362b;
  border-radius: 9px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  box-shadow: inset 0 0 0 2px rgba(255, 244, 234, 0.18), 0 2px 10px rgba(120, 30, 24, 0.28);
  transform: rotate(-7deg);
  opacity: 0;
  animation: stamp 0.5s cubic-bezier(0.34, 1.4, 0.5, 1) forwards;
  animation-delay: 1s;
}
.seal span {
  font-family: var(--cd-serif);
  font-weight: 700;
  font-size: clamp(1.4rem, 2.6vw, 2rem);
  line-height: 1;
  color: #faf2e6;
}
@keyframes stamp {
  0% { opacity: 0; transform: rotate(-7deg) scale(1.7); }
  60% { opacity: 1; transform: rotate(-7deg) scale(0.92); }
  100% { opacity: 1; transform: rotate(-7deg) scale(1); }
}

.epigraph {
  margin: 30px 0 0;
  font-family: var(--cd-serif);
  font-size: clamp(1.5rem, 3.4vw, 2.3rem);
  font-weight: 500;
  color: #2a241d;
  letter-spacing: 0.04em;
}
.sub {
  margin: 16px auto 0;
  max-width: 30em;
  font-size: 1.04rem;
  line-height: 1.7;
  color: #6b6053;
}
.actions { display: flex; gap: 14px; justify-content: center; margin-top: 38px; }
.btn {
  display: inline-flex;
  align-items: center;
  padding: 11px 28px;
  border-radius: 999px;
  font-size: 1rem;
  font-weight: 600;
  transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
}
.btn.primary { background: #b1542f; color: #fff; }
.btn.primary:hover { background: #c2603f; transform: translateY(-1px); }
.btn.ghost { border: 1px solid #d8cdb9; color: #2a2620; }
.btn.ghost:hover { border-color: #b1542f; transform: translateY(-1px); }

.scroll-cue {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: none;
  border: none;
  color: #8a8073;
  font-size: 0.86rem;
  letter-spacing: 0.12em;
  cursor: pointer;
  animation: bob 2.2s ease-in-out infinite;
}
@keyframes bob { 0%, 100% { transform: translateX(-50%) translateY(0); } 50% { transform: translateX(-50%) translateY(5px); } }

/* 入场：逐层浮现 */
.rise { opacity: 0; animation: rise 0.7s cubic-bezier(0.2, 0.7, 0.2, 1) forwards; animation-delay: var(--d, 0s); }
@keyframes rise { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }

@media (prefers-reduced-motion: reduce) {
  .rise, .seal, .brush path, .scroll-cue { animation: none !important; opacity: 1 !important; }
  .seal { transform: rotate(-7deg); }
  .brush path { stroke-dashoffset: 0; }
}

/* ===================== 目录（暖色） ===================== */
.below { max-width: 1060px; margin: 0 auto; padding: 80px 28px 110px; }
.hook { padding-bottom: 50px; border-bottom: 1px solid var(--cd-rule); }
.hook h2 { margin: 0; font-family: var(--cd-serif); font-size: 1.85rem; font-weight: 600; color: var(--vp-c-text-1); }
.hook-lead { margin: 14px 0 26px; font-size: 1.08rem; color: var(--vp-c-text-2); }
.chain { display: flex; align-items: center; flex-wrap: wrap; gap: 10px 14px; }
.node { padding: 9px 18px; border-radius: 10px; background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); font-weight: 600; }
.arrow { color: var(--vp-c-text-3); font-style: normal; }
.hook-foot { margin: 26px 0 0; color: var(--vp-c-text-2); }
.hook-foot b { color: var(--vp-c-text-1); }
.hook-foot a { color: var(--vp-c-brand-1); font-weight: 600; white-space: nowrap; }

.catalog { padding: 50px 0 20px; }
.catalog-intro { margin: 0 0 26px; color: var(--vp-c-text-3); font-size: 0.95rem; }
.group { margin-bottom: 44px; }
.group-head { display: flex; align-items: baseline; gap: 14px; margin-bottom: 18px; padding-bottom: 10px; border-bottom: 1px solid var(--cd-rule); flex-wrap: wrap; }
.group-head h3 { margin: 0; font-family: var(--cd-serif); font-size: 1.4rem; font-weight: 600; color: var(--vp-c-text-1); }
.group-desc { font-size: 0.92rem; color: var(--vp-c-text-3); }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 16px; }
.card { display: grid; grid-template-columns: auto 1fr; grid-template-rows: auto auto; column-gap: 16px; align-items: center; padding: 20px 22px; border: 1px solid var(--vp-c-border); border-radius: 14px; background: var(--vp-c-bg-elv); transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease; }
.card:hover { border-color: var(--vp-c-brand-3); transform: translateY(-3px); box-shadow: 0 10px 26px rgba(40, 30, 20, 0.09); }
.card .no { grid-row: 1 / 3; font-family: var(--cd-serif); font-size: 2.1rem; font-weight: 600; color: var(--vp-c-brand-2); line-height: 1; }
.card .ct { font-family: var(--cd-serif); font-size: 1.16rem; font-weight: 600; color: var(--vp-c-text-1); }
.card .cd { font-size: 0.9rem; line-height: 1.5; color: var(--vp-c-text-2); }

.howto { margin-top: 30px; padding: 44px 36px; border-radius: 16px; background: var(--vp-c-bg-soft); }
.howto h2 { margin: 0 0 26px; font-family: var(--cd-serif); font-size: 1.5rem; font-weight: 600; color: var(--vp-c-text-1); }
.hcols { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 30px; }
.hcol h4 { margin: 0 0 8px; font-size: 1.05rem; font-weight: 600; color: var(--vp-c-brand-1); }
.hcol p { margin: 0; font-size: 0.96rem; line-height: 1.7; color: var(--vp-c-text-2); }

@media (max-width: 640px) {
  .seal { right: -12px; top: -52px; }
  .below { padding: 56px 20px 72px; }
}
</style>
