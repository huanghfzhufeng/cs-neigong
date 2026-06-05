<script setup lang="ts">
import { withBase } from 'vitepress'
import { onMounted, onUnmounted, ref } from 'vue'
import heroImg from './assets/hero-a.png'
import brush from './assets/d-brush.png'
import mountains from './assets/d-mountains.png'
import t01 from './assets/t-01.png'
import t02 from './assets/t-02.png'
import t03 from './assets/t-03.png'
import t04 from './assets/t-04.png'
import t05 from './assets/t-05.png'
import t06 from './assets/t-06.png'
import t07 from './assets/t-07.png'
import t08 from './assets/t-08.png'
import t09 from './assets/t-09.png'

const GH = 'https://github.com/huanghfzhufeng/cs-neigong'

const tiles = [
  { no: '01', name: '计算机组成原理', desc: '机器到底怎么算', link: '/01-计算机组成原理/', img: t01 },
  { no: '02', name: '操作系统', desc: '资源怎么调度', link: '/02-操作系统/', img: t02 },
  { no: '03', name: '计算机网络', desc: '数据怎么跨机器送达', link: '/03-计算机网络/', img: t03 },
  { no: '04', name: '数据结构与算法', desc: '怎么存、怎么高效解', link: '/04-数据结构与算法/', img: t04 },
  { no: '05', name: 'MySQL', desc: '怎么可靠存取', link: '/05-MySQL/', img: t05 },
  { no: '06', name: '互联网架构演进', desc: '怎么扛住流量', link: '/06-互联网架构演进/', img: t06 },
  { no: '07', name: '系统质量属性与架构评估', desc: '怎么权衡好坏', link: '/07-系统质量属性与架构评估/', img: t07 },
  { no: '08', name: '软件工程', desc: '怎么把事做对', link: '/08-软件工程/', img: t08 },
  { no: '09', name: 'LLM 与 Agent 工程', desc: '怎么用模型把活干好', link: '/09-LLM与Agent工程/', img: t09 },
]

const mountainsEl = ref<HTMLElement>()
let io: IntersectionObserver | undefined
let raf = 0
function onScroll() {
  cancelAnimationFrame(raf)
  raf = requestAnimationFrame(() => {
    const el = mountainsEl.value
    if (el) {
      const r = el.getBoundingClientRect()
      const off = (window.innerHeight - r.top) * 0.06
      el.style.setProperty('--py', `${off.toFixed(1)}px`)
    }
  })
}
function scrollDown() {
  document.querySelector('.scroll-target')?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  document.documentElement.classList.add('home-hero')
  io = new IntersectionObserver(
    (entries) =>
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('in')
          io!.unobserve(e.target)
        }
      }),
    { threshold: 0.16 },
  )
  document.querySelectorAll('.reveal').forEach((el) => io!.observe(el))
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})
onUnmounted(() => {
  document.documentElement.classList.remove('home-hero')
  io?.disconnect()
  window.removeEventListener('scroll', onScroll)
  cancelAnimationFrame(raf)
})
</script>

<template>
  <div class="landing">
    <!-- ===== 扉页 ===== -->
    <section class="codex">
      <div class="grain"></div>
      <header class="cx-top">
        <span class="wordmark">内功</span>
        <a class="gh" :href="GH" target="_blank" rel="noreferrer">GitHub</a>
      </header>

      <div class="cover">
        <div class="art">
          <div class="art-glow"></div>
          <img :src="heroImg" alt="武者于山中静坐运功" />
          <div class="seal" aria-hidden="true"><span>内</span><span>功</span></div>
        </div>

        <h1 class="epigraph">招式人人会，内功定高下。</h1>
        <img class="ul" :src="brush" alt="" aria-hidden="true" />
        <p class="sub">模型什么都能做——做得好不好，看你的内功有多深。</p>

        <div class="actions">
          <a class="btn primary" :href="withBase('/00-导读')">开始修炼</a>
          <a class="btn ghost" :href="GH" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </div>

      <button class="scroll-cue" @click="scrollDown" aria-label="向下">↓</button>
    </section>

    <span class="scroll-target"></span>

    <!-- ===== 九门内功（图为主） ===== -->
    <section class="dojo">
      <div class="dojo-head reveal">
        <h2>九门内功</h2>
        <p>循序修炼，由内而外 · 持续增补</p>
      </div>
      <div class="grid">
        <a
          v-for="(t, i) in tiles"
          :key="t.no"
          class="tile reveal"
          :style="{ '--i': i }"
          :href="withBase(t.link)"
        >
          <div class="tile-img"><img :src="t.img" :alt="t.name" loading="lazy" /></div>
          <div class="tile-cap">
            <span class="tn">{{ t.no }}</span>
            <span class="tt">{{ t.name }}</span>
            <span class="td">{{ t.desc }}</span>
          </div>
        </a>
      </div>
    </section>

    <!-- ===== 远山（视差） ===== -->
    <div class="range" ref="mountainsEl">
      <img :src="mountains" alt="" aria-hidden="true" />
      <div class="range-words reveal">
        <p>九份是一块块砖，连起来才是一套体系。</p>
        <a :href="withBase('/00-导读')">看脉络怎么贯通 →</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ===================== 扉页 ===================== */
.codex {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: radial-gradient(120% 100% at 50% 28%, #f7efdc 0%, #f2e8d2 55%, #ece0c6 100%);
}
.landing { background: #f2e8d2; }
.grain {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.45;
  mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E");
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
.wordmark { font-family: var(--cd-serif); font-size: 1.3rem; font-weight: 600; color: #2a2620; letter-spacing: 0.06em; }
.gh { color: #6b6053; font-size: 0.9rem; font-weight: 500; }
.gh:hover { color: #2a2620; }

.cover { position: relative; z-index: 2; text-align: center; padding: 0 24px; max-width: 44em; }

/* 主插画：墨色“显影”入场 + 边缘融入纸面 */
.art { position: relative; display: inline-block; margin: 0 auto; }
.art img {
  position: relative;
  z-index: 2;
  display: block;
  width: clamp(280px, 38vw, 480px);
  height: auto;
  -webkit-mask-image: radial-gradient(circle at 50% 50%, #000 72%, transparent 97%);
  mask-image: radial-gradient(circle at 50% 50%, #000 72%, transparent 97%);
  animation: develop 1.6s cubic-bezier(0.2, 0.7, 0.2, 1) 0.1s both;
}
@keyframes develop {
  from { opacity: 0; transform: scale(0.94); filter: blur(12px); }
  to { opacity: 1; transform: none; filter: blur(0); }
}
.art-glow {
  position: absolute;
  inset: 4%;
  z-index: 1;
  background: radial-gradient(circle at 50% 46%, rgba(194, 96, 63, 0.14), transparent 62%);
  filter: blur(20px);
  animation: glow 6s ease-in-out infinite;
}
@keyframes glow { 0%, 100% { opacity: 0.8; transform: scale(1); } 50% { opacity: 1; transform: scale(1.04); } }

.seal {
  position: absolute;
  right: 9%;
  bottom: 7%;
  z-index: 3;
  width: clamp(42px, 5vw, 58px);
  height: clamp(42px, 5vw, 58px);
  background: #b5362b;
  border-radius: 7px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 0 0 1.5px rgba(255, 244, 234, 0.2), 0 2px 8px rgba(120, 30, 24, 0.3);
  transform: rotate(-7deg);
  opacity: 0;
  animation: stamp 0.5s cubic-bezier(0.34, 1.4, 0.5, 1) 1.4s forwards;
}
.seal span { font-family: var(--cd-serif); font-weight: 700; font-size: clamp(1rem, 1.7vw, 1.35rem); line-height: 1.02; color: #faf2e6; }
@keyframes stamp {
  0% { opacity: 0; transform: rotate(-7deg) scale(1.7); }
  60% { opacity: 1; transform: rotate(-7deg) scale(0.92); }
  100% { opacity: 1; transform: rotate(-7deg) scale(1); }
}

.epigraph {
  margin: 6px 0 0;
  font-family: var(--cd-serif);
  font-size: clamp(1.8rem, 4.2vw, 2.9rem);
  font-weight: 600;
  color: #2a241d;
  letter-spacing: 0.04em;
  opacity: 0;
  animation: fade 0.9s ease 0.7s forwards;
}
/* 毛笔下划线：从左到右“画”出来 */
.ul {
  display: block;
  width: clamp(200px, 28vw, 320px);
  height: auto;
  margin: -2px auto 0;
  clip-path: inset(0 100% 0 0);
  animation: wipe 0.9s cubic-bezier(0.65, 0, 0.35, 1) 1s forwards;
}
@keyframes wipe { to { clip-path: inset(0 0 0 0); } }
.sub { margin: 14px auto 0; max-width: 28em; font-size: 1.02rem; color: #6b6053; opacity: 0; animation: fade 0.9s ease 1.1s forwards; }
.actions { display: flex; gap: 14px; justify-content: center; margin-top: 30px; opacity: 0; animation: fade 0.9s ease 1.3s forwards; }
@keyframes fade { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }

.btn { display: inline-flex; align-items: center; padding: 11px 28px; border-radius: 999px; font-size: 1rem; font-weight: 600; transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease; }
.btn.primary { background: #b1542f; color: #fff; }
.btn.primary:hover { background: #c2603f; transform: translateY(-1px); }
.btn.ghost { border: 1px solid #d8cdb9; color: #2a2620; }
.btn.ghost:hover { border-color: #b1542f; transform: translateY(-1px); }

.scroll-cue {
  position: absolute;
  bottom: 26px;
  left: 50%;
  transform: translateX(-50%);
  background: none;
  border: none;
  color: #a89c8a;
  font-size: 1.3rem;
  cursor: pointer;
  opacity: 0;
  animation: fade 1s ease 1.8s forwards, breathe 2.6s ease-in-out 2.4s infinite;
}
@keyframes breathe { 0%, 100% { opacity: 0.45; } 50% { opacity: 0.9; } }

/* ===================== 九门内功 ===================== */
.dojo { max-width: 1140px; margin: 0 auto; padding: 96px 28px 40px; }
.dojo-head { text-align: center; margin-bottom: 42px; }
.dojo-head h2 { margin: 0; font-family: var(--cd-serif); font-size: 2rem; font-weight: 600; color: #2a241d; letter-spacing: 0.08em; }
.dojo-head p { margin: 10px 0 0; color: #8a8073; font-size: 0.96rem; letter-spacing: 0.04em; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.tile {
  display: block;
  border-radius: 16px;
  overflow: hidden;
  background: #fffdf9;
  border: 1px solid #ece3d2;
  text-decoration: none;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.tile:hover { transform: translateY(-4px); border-color: #d9a890; box-shadow: 0 16px 34px rgba(60, 40, 25, 0.12); }
.tile-img { background: #f2e8d2; }
.tile-img img { display: block; width: 100%; aspect-ratio: 1 / 1; object-fit: cover; }
.tile-cap { display: flex; align-items: baseline; gap: 10px; padding: 16px 18px 18px; border-top: 1px solid #f0e8d8; }
.tile-cap .tn { font-family: var(--cd-serif); font-size: 1.2rem; font-weight: 600; color: #c2603f; }
.tile-cap .tt { font-family: var(--cd-serif); font-size: 1.08rem; font-weight: 600; color: #2a241d; }
.tile-cap .td { margin-left: auto; font-size: 0.84rem; color: #8a8073; white-space: nowrap; }

/* 滚动入场：上浮 + 轻微缩放，逐个错开（refined） */
.reveal { opacity: 0; transform: translateY(28px) scale(0.985); transition: opacity 0.8s ease, transform 0.8s cubic-bezier(0.2, 0.7, 0.2, 1); transition-delay: calc(var(--i, 0) * 0.07s); }
.reveal.in { opacity: 1; transform: none; }

/* ===================== 远山（视差） ===================== */
.range { position: relative; margin-top: 40px; overflow: hidden; }
.range img { display: block; width: 100%; object-fit: cover; max-height: 420px; transform: translateY(var(--py, 0)); will-change: transform; opacity: 0.92; }
.range-words { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 12px; }
.range-words p { margin: 0; font-family: var(--cd-serif); font-size: clamp(1.2rem, 2.6vw, 1.7rem); color: #2f2618; text-shadow: 0 2px 18px rgba(247, 240, 224, 0.96), 0 0 4px rgba(247, 240, 224, 0.9); }
.range-words a { color: #a8431f; font-weight: 700; text-shadow: 0 2px 14px rgba(247, 240, 224, 0.96); }

@media (prefers-reduced-motion: reduce) {
  .art img, .seal, .epigraph, .ul, .sub, .actions, .scroll-cue { animation: none !important; opacity: 1 !important; clip-path: none !important; }
  .seal { transform: rotate(-7deg); }
  .reveal { opacity: 1; transform: none; transition: none; }
}
@media (max-width: 860px) { .grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) {
  .grid { grid-template-columns: 1fr; }
  .dojo { padding: 64px 20px 30px; }
}
</style>
