<script setup lang="ts">
import { withBase } from 'vitepress'
import { onMounted, onUnmounted, ref } from 'vue'
import center from './assets/hero-cultivator.webp'
import mountains from './assets/d-mountains.webp'
import t01 from './assets/t-01.webp'
import t02 from './assets/t-02.webp'
import t03 from './assets/t-03.webp'
import t04 from './assets/t-04.webp'
import t05 from './assets/t-05.webp'
import t06 from './assets/t-06.webp'
import t07 from './assets/t-07.webp'
import t08 from './assets/t-08.webp'
import t09 from './assets/t-09.webp'

const GH = 'https://github.com/huanghfzhufeng/cs-neigong'
const IMG: Record<string, string> = {
  '01-计算机组成原理': t01, '02-操作系统': t02, '03-计算机网络': t03,
  '04-数据结构与算法': t04, '05-MySQL': t05, '06-互联网架构演进': t06,
  '07-系统质量属性与架构评估': t07, '08-软件工程': t08, '09-LLM与Agent工程': t09,
}

// 环绕的九枚“内功印记”
const RAW = [
  { short: '组成原理', slug: '01-计算机组成原理' },
  { short: '操作系统', slug: '02-操作系统' },
  { short: '计算机网络', slug: '03-计算机网络' },
  { short: '数据结构', slug: '04-数据结构与算法' },
  { short: 'MySQL', slug: '05-MySQL' },
  { short: '架构演进', slug: '06-互联网架构演进' },
  { short: '架构评估', slug: '07-系统质量属性与架构评估' },
  { short: '软件工程', slug: '08-软件工程' },
  { short: 'LLM·Agent', slug: '09-LLM与Agent工程' },
]
const emblems = RAW.map((e, i) => {
  const a = ((i * 360) / RAW.length - 90) * (Math.PI / 180)
  const x = 50 + 39 * Math.cos(a)
  const y = 50 + 39 * Math.sin(a)
  return { ...e, img: IMG[e.slug], link: `/${e.slug}/`, x, y, above: y < 44, d: 0.5 + i * 0.09 }
})

// 下方目录（按层次分组，自动同步）
import site from '../sidebars.json'
const DESC: Record<string, string> = {
  '01-计算机组成原理': '机器到底怎么算', '02-操作系统': '资源怎么调度',
  '03-计算机网络': '数据怎么跨机器送达', '04-数据结构与算法': '怎么存、怎么高效解',
  '05-MySQL': '怎么可靠存取', '06-互联网架构演进': '怎么扛住流量',
  '07-系统质量属性与架构评估': '怎么权衡好坏', '08-软件工程': '怎么把事做对',
  '09-LLM与Agent工程': '怎么用模型把活干好',
}
const GDESC: Record<string, string> = {
  '地基': '机器与数据怎么运转', '运行与连接': '程序怎么跑、请求怎么到',
  '数据与架构': '怎么可靠存取、怎么扛住流量', '方法与上层': '怎么把事做对、用好模型',
}
const groups = (site.nav as any[]).filter((n) => Array.isArray(n.items)).map((g) => ({
  title: g.text, desc: GDESC[g.text] ?? '',
  items: (g.items as any[]).map((it) => {
    const [no, name] = (it.text as string).split(' · ')
    const slug = (it.link as string).replace(/\//g, '')
    return { no, name: name ?? it.text, desc: DESC[slug] ?? '', link: it.link, img: IMG[slug] }
  }),
}))

const mountainsEl = ref<HTMLElement>()
let io: IntersectionObserver | undefined
let raf = 0
function onScroll() {
  cancelAnimationFrame(raf)
  raf = requestAnimationFrame(() => {
    const el = mountainsEl.value
    if (el) {
      const r = el.getBoundingClientRect()
      el.style.setProperty('--py', `${((innerHeight - r.top) * 0.05).toFixed(1)}px`)
    }
  })
}
function scrollDown() {
  document.querySelector('.below')?.scrollIntoView({ behavior: 'smooth' })
}
onMounted(() => {
  document.documentElement.classList.add('home-hero')
  io = new IntersectionObserver(
    (es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io!.unobserve(e.target) } }),
    { threshold: 0.15 },
  )
  document.querySelectorAll('.reveal').forEach((el) => io!.observe(el))
  addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})
onUnmounted(() => {
  document.documentElement.classList.remove('home-hero')
  io?.disconnect()
  removeEventListener('scroll', onScroll)
  cancelAnimationFrame(raf)
})
</script>

<template>
  <div class="landing">
    <!-- ===== 沉浸式扉页：修炼者居中，九门环绕 ===== -->
    <section class="codex">
      <div class="grain"></div>
      <header class="cx-top">
        <span class="wordmark">内功</span>
        <a class="gh" :href="GH" target="_blank" rel="noreferrer">GitHub</a>
      </header>

      <div class="stage">
        <svg class="rings" viewBox="0 0 100 100" aria-hidden="true">
          <circle class="r-out" cx="50" cy="50" r="39" />
          <circle class="r-in" cx="50" cy="50" r="26" />
        </svg>

        <div class="core">
          <div class="core-glow"></div>
          <span class="core-medal"><img :src="center" alt="内功修炼者" /></span>
          <div class="seal" aria-hidden="true"><span>内</span><span>功</span></div>
        </div>

        <a
          v-for="e in emblems"
          :key="e.slug"
          class="emblem"
          :class="{ above: e.above }"
          :style="{ left: e.x + '%', top: e.y + '%', '--d': e.d + 's' }"
          :href="withBase(e.link)"
        >
          <span class="medal"><img :src="e.img" :alt="e.short" /></span>
          <span class="elabel">{{ e.short }}</span>
        </a>
      </div>

      <div class="hero-foot">
        <p class="tagline">招式人人会，内功定高下</p>
        <p class="subline">模型什么都能做——做得好不好，看你的内功有多深。</p>
        <div class="actions">
          <a class="btn primary" :href="withBase('/00-导读')">开始修炼</a>
          <a class="btn ghost" :href="GH" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </div>
      <button class="scroll-cue" @click="scrollDown" aria-label="向下">↓</button>
    </section>

    <!-- ===== 下方：循序修炼（图为主，分层） ===== -->
    <div class="below">
      <div class="dojo-head reveal"><h2>循序修炼</h2><p>由内而外，九门一脉相承 · 持续增补</p></div>
      <section v-for="g in groups" :key="g.title" class="layer">
        <div class="layer-head reveal"><h3>{{ g.title }}</h3><span>{{ g.desc }}</span></div>
        <div class="grid">
          <a v-for="(t, i) in g.items" :key="t.no" class="tile reveal" :style="{ '--i': i }" :href="withBase(t.link)">
            <span class="tile-img"><img :src="t.img" :alt="t.name" loading="lazy" /></span>
            <span class="tile-cap"><b>{{ t.no }}</b><span class="tt">{{ t.name }}</span><span class="td">{{ t.desc }}</span></span>
          </a>
        </div>
      </section>
    </div>

    <div class="range" ref="mountainsEl">
      <img :src="mountains" alt="" aria-hidden="true" loading="lazy" />
      <div class="range-words reveal">
        <p>九门是一块块砖，连起来才是一套体系。</p>
        <a :href="withBase('/00-导读')">看脉络怎么贯通 →</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.landing { background: #f2e8d2; }

/* ===================== 沉浸式扉页 ===================== */
.codex {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: radial-gradient(115% 90% at 50% 42%, #f8f0de 0%, #f2e8d2 54%, #e7d9be 100%);
}
.grain {
  position: absolute; inset: 0; pointer-events: none; opacity: 0.4; mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E");
}
.cx-top { position: absolute; top: 24px; left: 0; right: 0; display: flex; justify-content: space-between; padding: 0 36px; z-index: 6; }
.wordmark { font-family: var(--cd-serif); font-size: 1.3rem; font-weight: 600; color: #2a2620; letter-spacing: 0.06em; }
.gh { color: #6b6053; font-size: 0.9rem; font-weight: 500; }
.gh:hover { color: #2a2620; }

.stage { position: relative; width: min(94vw, 78vh, 880px); height: min(94vw, 78vh, 880px); margin: 0 auto; flex: none; }
.rings { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.rings circle { fill: none; stroke: #b98a63; }
.r-out { stroke-width: 0.25; opacity: 0.35; stroke-dasharray: 1.6 2.4; transform-origin: 50% 50%; animation: spin 160s linear infinite; }
.r-in { stroke-width: 0.2; opacity: 0.22; }
@keyframes spin { to { transform: rotate(360deg); } }

/* 中心修炼者 */
.core { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 33%; height: 33%; z-index: 3; }
.core-glow { position: absolute; inset: -22%; border-radius: 50%; background: radial-gradient(circle, rgba(194, 96, 63, 0.2), transparent 66%); filter: blur(14px); animation: breathe 6s ease-in-out infinite; }
.core-medal {
  position: absolute; inset: 0; border-radius: 50%; overflow: hidden; background: #f2e8d2;
  box-shadow: inset 0 0 0 1.5px rgba(120, 80, 50, 0.18), 0 8px 30px rgba(90, 55, 30, 0.16);
  animation: develop 1.5s cubic-bezier(0.2, 0.7, 0.2, 1) 0.1s both;
}
.core-medal img { width: 100%; height: 100%; object-fit: cover; transform: scale(1.06); }
.seal {
  position: absolute; right: -4%; bottom: 2%; z-index: 4; width: 30%; height: 30%; max-width: 60px; max-height: 60px;
  background: #b5362b; border-radius: 7px; display: flex; flex-direction: column; align-items: center; justify-content: center;
  box-shadow: inset 0 0 0 1.5px rgba(255, 244, 234, 0.2), 0 2px 8px rgba(120, 30, 24, 0.3);
  transform: rotate(-7deg); opacity: 0; animation: stamp 0.5s cubic-bezier(0.34, 1.4, 0.5, 1) 1.5s forwards;
}
.seal span { font-family: var(--cd-serif); font-weight: 700; font-size: clamp(0.8rem, 1.5vw, 1.1rem); line-height: 1.04; color: #faf2e6; }

/* 九枚印记 */
.emblem {
  position: absolute; transform: translate(-50%, -50%); z-index: 3;
  display: flex; flex-direction: column; align-items: center; gap: 7px;
  width: 23%; text-decoration: none;
  opacity: 0; animation: pop 0.6s cubic-bezier(0.34, 1.3, 0.5, 1) var(--d) both;
}
.emblem.above { flex-direction: column-reverse; }
.medal {
  width: 100%; aspect-ratio: 1; border-radius: 50%; overflow: hidden; background: #f2e8d2;
  box-shadow: inset 0 0 0 1px rgba(120, 80, 50, 0.16), 0 5px 16px rgba(90, 55, 30, 0.12);
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}
.medal img { width: 100%; height: 100%; object-fit: cover; transform: scale(1.04); }
.emblem:hover { z-index: 5; }
.emblem:hover .medal { transform: scale(1.1); box-shadow: inset 0 0 0 1px rgba(177, 84, 47, 0.4), 0 12px 26px rgba(90, 55, 30, 0.2); }
.elabel { font-size: clamp(0.74rem, 1.5vw, 0.95rem); font-weight: 600; color: #4a4034; white-space: nowrap; }
.emblem:hover .elabel { color: #b1542f; }

.hero-foot { position: relative; z-index: 4; text-align: center; margin-top: 18px; opacity: 0; animation: fade 0.9s ease 1.3s forwards; }
.tagline { margin: 0; font-family: var(--cd-serif); font-size: clamp(1.5rem, 3.4vw, 2.2rem); font-weight: 600; color: #2a241d; letter-spacing: 0.05em; }
.subline { margin: 10px 0 0; font-size: 0.98rem; color: #6b6053; }
.actions { display: flex; gap: 14px; justify-content: center; margin-top: 24px; }
.btn { display: inline-flex; align-items: center; padding: 11px 28px; border-radius: 999px; font-size: 1rem; font-weight: 600; transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease; }
.btn.primary { background: #b1542f; color: #fff; }
.btn.primary:hover { background: #c2603f; transform: translateY(-1px); }
.btn.ghost { border: 1px solid #d2c5ac; color: #2a2620; }
.btn.ghost:hover { border-color: #b1542f; transform: translateY(-1px); }
.scroll-cue { position: absolute; bottom: 22px; left: 50%; transform: translateX(-50%); background: none; border: none; color: #a89c8a; font-size: 1.3rem; cursor: pointer; opacity: 0; animation: fade 1s ease 1.9s forwards, breathe 2.6s ease-in-out 2.6s infinite; }

@keyframes develop { from { opacity: 0; transform: scale(0.92); filter: blur(10px); } to { opacity: 1; transform: none; filter: blur(0); } }
@keyframes pop { from { opacity: 0; transform: translate(-50%, -50%) scale(0.4); } to { opacity: 1; transform: translate(-50%, -50%) scale(1); } }
@keyframes fade { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
@keyframes breathe { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }

/* ===================== 下方目录 ===================== */
.below { max-width: 1120px; margin: 0 auto; padding: 92px 28px 50px; }
.dojo-head { text-align: center; margin-bottom: 50px; }
.dojo-head h2 { margin: 0; font-family: var(--cd-serif); font-size: 2rem; font-weight: 600; color: #2a241d; letter-spacing: 0.1em; }
.dojo-head p { margin: 10px 0 0; color: #8a8073; font-size: 0.96rem; }
.layer { margin-bottom: 40px; }
.layer-head { display: flex; align-items: baseline; gap: 14px; margin-bottom: 18px; padding-bottom: 10px; border-bottom: 1px solid #e3d8c2; }
.layer-head h3 { margin: 0; font-family: var(--cd-serif); font-size: 1.35rem; font-weight: 600; color: #2a241d; }
.layer-head span { font-size: 0.9rem; color: #8a8073; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.tile { display: block; border-radius: 14px; overflow: hidden; background: #fffdf9; border: 1px solid #e6dcc8; text-decoration: none; transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease; }
.tile:hover { transform: translateY(-4px); border-color: #d9a890; box-shadow: 0 14px 30px rgba(60, 40, 25, 0.12); }
.tile-img { display: block; background: #f2e8d2; }
.tile-img img { display: block; width: 100%; aspect-ratio: 16 / 11; object-fit: cover; }
.tile-cap { display: flex; align-items: baseline; gap: 9px; padding: 14px 16px 16px; border-top: 1px solid #f0e8d8; }
.tile-cap b { font-family: var(--cd-serif); font-size: 1.05rem; color: #c2603f; }
.tile-cap .tt { font-family: var(--cd-serif); font-size: 1rem; font-weight: 600; color: #2a241d; }
.tile-cap .td { margin-left: auto; font-size: 0.8rem; color: #8a8073; white-space: nowrap; }

.reveal { opacity: 0; transform: translateY(26px); transition: opacity 0.7s ease, transform 0.7s cubic-bezier(0.2, 0.7, 0.2, 1); transition-delay: calc(var(--i, 0) * 0.06s); }
.reveal.in { opacity: 1; transform: none; }

.range { position: relative; overflow: hidden; }
.range img { display: block; width: 100%; object-fit: cover; max-height: 440px; transform: translateY(var(--py, 0)); will-change: transform; }
.range-words { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 10px; }
.range-words p { margin: 0; font-family: var(--cd-serif); font-size: clamp(1.2rem, 2.6vw, 1.7rem); color: #2f2618; text-shadow: 0 2px 18px rgba(247, 240, 224, 0.96), 0 0 4px rgba(247, 240, 224, 0.9); }
.range-words a { color: #a8431f; font-weight: 700; text-shadow: 0 2px 14px rgba(247, 240, 224, 0.96); }

@media (prefers-reduced-motion: reduce) {
  .core-medal, .seal, .emblem, .hero-foot, .scroll-cue, .r-out { animation: none !important; opacity: 1 !important; }
  .emblem { transform: translate(-50%, -50%); }
  .seal { transform: rotate(-7deg); }
  .reveal { opacity: 1; transform: none; transition: none; }
}
@media (max-width: 760px) { .grid { grid-template-columns: repeat(2, 1fr); } .elabel { font-size: 0.7rem; } }
@media (max-width: 520px) { .grid { grid-template-columns: 1fr; } .below { padding: 60px 20px 30px; } }
</style>
