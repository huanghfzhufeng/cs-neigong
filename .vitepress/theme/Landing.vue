<script setup lang="ts">
import { withBase } from 'vitepress'
import { onMounted, onUnmounted, ref } from 'vue'
import center from './assets/hero-cultivator.webp'
import mountains from './assets/d-mountains.webp'
import m01 from './assets/m-01.webp'
import m02 from './assets/m-02.webp'
import m03 from './assets/m-03.webp'
import m04 from './assets/m-04.webp'
import m05 from './assets/m-05.webp'
import m06 from './assets/m-06.webp'
import m07 from './assets/m-07.webp'
import m08 from './assets/m-08.webp'
import m09 from './assets/m-09.webp'

const GH = 'https://github.com/huanghfzhufeng/cs-neigong'

const forms = [
  { n: '一', name: '计算机组成原理', desc: '机器到底怎么算', img: m01, link: '/01-计算机组成原理/' },
  { n: '二', name: '操作系统', desc: '资源怎么调度', img: m02, link: '/02-操作系统/' },
  { n: '三', name: '计算机网络', desc: '数据怎么跨机器送达', img: m03, link: '/03-计算机网络/' },
  { n: '四', name: '数据结构与算法', desc: '怎么存、怎么高效解', img: m04, link: '/04-数据结构与算法/' },
  { n: '五', name: 'MySQL', desc: '怎么可靠存取', img: m05, link: '/05-MySQL/' },
  { n: '六', name: '互联网架构演进', desc: '怎么扛住流量', img: m06, link: '/06-互联网架构演进/' },
  { n: '七', name: '系统质量属性与架构评估', desc: '怎么权衡好坏', img: m07, link: '/07-系统质量属性与架构评估/' },
  { n: '八', name: '软件工程', desc: '怎么把事做对', img: m08, link: '/08-软件工程/' },
  { n: '九', name: 'LLM 与 Agent 工程', desc: '怎么用模型把活干好', img: m09, link: '/09-LLM与Agent工程/' },
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
      el.style.setProperty('--py', `${((innerHeight - r.top) * 0.05).toFixed(1)}px`)
    }
  })
}
function scrollDown() {
  document.querySelector('.forms-sec')?.scrollIntoView({ behavior: 'smooth' })
}
onMounted(() => {
  document.documentElement.classList.add('home-hero')
  io = new IntersectionObserver(
    (es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io!.unobserve(e.target) } }),
    { threshold: 0.14 },
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
    <!-- ===== 扉页：心法 ===== -->
    <section class="codex">
      <div class="grain"></div>
      <div class="watermark">功</div>
      <header class="cx-top">
        <span class="wordmark">内功</span>
        <a class="gh" :href="GH" target="_blank" rel="noreferrer">GitHub</a>
      </header>

      <div class="cover">
        <p class="kicker">内功心法 · 计算机底层图文详解</p>
        <div class="art">
          <div class="art-glow"></div>
          <span class="art-medal"><img :src="center" alt="内功修炼者" /></span>
        </div>
        <h1 class="epigraph">招式人人会，内功定高下</h1>
        <div class="lead">
          <p>vibe coding 时代，模型什么都能做——做得好不好，看你的内功有多深。这套手册把计算机底层一份份讲透：是什么、为什么、解决什么、怎么用。</p>
          <p>懂了底层，你才压得住模型，而不是把垃圾越堆越高。人和模型相互成就，<b>你的上限，决定它能帮你到哪</b>。</p>
        </div>
        <div class="actions">
          <a class="btn primary" :href="withBase('/00-导读')">开始修炼</a>
          <a class="btn ghost" :href="GH" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </div>
      <button class="scroll-cue" @click="scrollDown" aria-label="向下">内功九式 ↓</button>
    </section>

    <!-- ===== 内功九式（拳谱） ===== -->
    <section class="forms-sec">
      <div class="forms-head reveal">
        <h2>内功九式</h2>
        <p>循序修炼，由浅入深 · 持续增补</p>
      </div>
      <div class="forms">
        <a v-for="(f, i) in forms" :key="f.n" class="form reveal" :style="{ '--i': i }" :href="withBase(f.link)">
          <span class="form-no">第 {{ f.n }} 式</span>
          <span class="form-img"><img :src="f.img" :alt="f.name" loading="lazy" /></span>
          <span class="form-name">{{ f.name }}</span>
          <span class="form-desc">{{ f.desc }}</span>
        </a>
      </div>
    </section>

    <!-- ===== 远山 ===== -->
    <div class="range" ref="mountainsEl">
      <img :src="mountains" alt="" aria-hidden="true" loading="lazy" />
      <div class="range-words reveal">
        <p>九式是一招招式，连起来才是一身内功。</p>
        <a :href="withBase('/00-导读')">看脉络怎么贯通 →</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.landing { background: #f2e8d2; }

/* ===================== 扉页 ===================== */
.codex {
  position: relative; min-height: 92vh; overflow: hidden;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  background: radial-gradient(115% 90% at 50% 40%, #f8f0de 0%, #f2e8d2 56%, #e7d9be 100%);
}
.grain {
  position: absolute; inset: 0; pointer-events: none; opacity: 0.4; mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E");
}
.watermark { position: absolute; right: -4vmin; bottom: -16vmin; font-family: var(--cd-serif); font-weight: 600; font-size: 58vmin; line-height: 1; color: #3a2e22; opacity: 0.035; pointer-events: none; user-select: none; }
.cx-top { position: absolute; top: 24px; left: 0; right: 0; display: flex; justify-content: space-between; padding: 0 36px; z-index: 6; }
.wordmark { font-family: var(--cd-serif); font-size: 1.3rem; font-weight: 600; color: #2a2620; letter-spacing: 0.06em; }
.gh { color: #6b6053; font-size: 0.9rem; font-weight: 500; }
.gh:hover { color: #2a2620; }

.cover { position: relative; z-index: 2; text-align: center; padding: 0 24px; max-width: 42em; }
.kicker { margin: 0 0 22px; color: #b1542f; font-size: 0.84rem; font-weight: 600; letter-spacing: 0.22em; }
.art { position: relative; display: inline-block; }
.art-medal {
  display: block; width: clamp(220px, 24vw, 300px); aspect-ratio: 1; border-radius: 50%; overflow: hidden; background: #f2e8d2;
  box-shadow: inset 0 0 0 1.5px rgba(120, 80, 50, 0.16), 0 10px 34px rgba(90, 55, 30, 0.16);
  animation: develop 1.5s cubic-bezier(0.2, 0.7, 0.2, 1) 0.1s both;
}
.art-medal img { width: 100%; height: 100%; object-fit: cover; transform: scale(1.05); }
.art-glow { position: absolute; inset: -16%; border-radius: 50%; background: radial-gradient(circle, rgba(194, 96, 63, 0.16), transparent 64%); filter: blur(16px); animation: breathe 6s ease-in-out infinite; }
.epigraph { margin: 26px 0 0; font-family: var(--cd-serif); font-size: clamp(1.8rem, 4.4vw, 2.9rem); font-weight: 600; color: #2a241d; letter-spacing: 0.05em; opacity: 0; animation: fade 0.9s ease 0.6s forwards; }
.sub { margin: 14px auto 0; max-width: 28em; font-size: 1.02rem; color: #6b6053; opacity: 0; animation: fade 0.9s ease 0.85s forwards; }
.actions { display: flex; gap: 14px; justify-content: center; margin-top: 30px; opacity: 0; animation: fade 0.9s ease 1.05s forwards; }
.btn { display: inline-flex; align-items: center; padding: 11px 28px; border-radius: 999px; font-size: 1rem; font-weight: 600; transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease; }
.btn.primary { background: #b1542f; color: #fff; }
.btn.primary:hover { background: #c2603f; transform: translateY(-1px); }
.btn.ghost { border: 1px solid #d2c5ac; color: #2a2620; }
.btn.ghost:hover { border-color: #b1542f; transform: translateY(-1px); }
.scroll-cue { position: absolute; bottom: 26px; left: 50%; transform: translateX(-50%); background: none; border: none; color: #8a8073; font-size: 0.84rem; letter-spacing: 0.14em; cursor: pointer; opacity: 0; animation: fade 1s ease 1.6s forwards, breathe 2.8s ease-in-out 2.2s infinite; }

@keyframes develop { from { opacity: 0; transform: scale(0.92); filter: blur(10px); } to { opacity: 1; transform: none; filter: blur(0); } }
@keyframes fade { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
@keyframes breathe { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }

/* hero 宣言（首屏直出，不另开段落） */
.lead { max-width: 33em; margin: 20px auto 0; opacity: 0; animation: fade 0.9s ease 0.85s forwards; }
.lead p { margin: 0 0 10px; font-size: 1.05rem; line-height: 1.92; color: #5f574b; }
.lead p:last-child { margin-bottom: 0; }
.lead b { color: #2a241d; font-weight: 600; }

/* ===================== 内功九式 ===================== */
.forms-sec { max-width: 1180px; margin: 0 auto; padding: 86px 28px 60px; }
.forms-head { text-align: center; margin-bottom: 48px; }
.forms-head h2 { margin: 0; font-family: var(--cd-serif); font-size: 2.1rem; font-weight: 600; color: #2a241d; letter-spacing: 0.14em; }
.forms-head p { margin: 10px 0 0; color: #8a8073; font-size: 0.96rem; letter-spacing: 0.04em; }
.forms { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.form {
  display: flex; flex-direction: column; align-items: center; text-align: center;
  padding: 26px 18px 22px; border-radius: 12px; background: #f3ecdb;
  border: 1px solid #ddd0b6; box-shadow: inset 0 0 0 3px #f3ecdb, inset 0 0 0 4px #e3d6bd;
  text-decoration: none; transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}
.form:hover { transform: translateY(-5px); border-color: #c98b62; box-shadow: inset 0 0 0 3px #f3ecdb, inset 0 0 0 4px #e3d6bd, 0 18px 36px rgba(70, 45, 25, 0.14); }
.form-no { font-family: var(--cd-serif); font-size: 0.95rem; font-weight: 600; color: #b1542f; letter-spacing: 0.16em; }
.form-img { display: block; width: 80%; margin: 10px 0 14px; }
.form-img img {
  display: block; width: 100%; aspect-ratio: 1 / 1; object-fit: cover;
  -webkit-mask-image: radial-gradient(circle at 50% 47%, #000 70%, transparent 95%);
  mask-image: radial-gradient(circle at 50% 47%, #000 70%, transparent 95%);
}
.form-name { font-family: var(--cd-serif); font-size: 1.2rem; font-weight: 600; color: #2a241d; }
.form-desc { margin-top: 5px; font-size: 0.88rem; color: #8a8073; }

.reveal { opacity: 0; transform: translateY(28px) scale(0.99); transition: opacity 0.7s ease, transform 0.7s cubic-bezier(0.2, 0.7, 0.2, 1); transition-delay: calc(var(--i, 0) * 0.06s); }
.reveal.in { opacity: 1; transform: none; }

/* ===================== 远山 ===================== */
.range { position: relative; overflow: hidden; }
.range img { display: block; width: 100%; object-fit: cover; max-height: 440px; transform: translateY(var(--py, 0)); will-change: transform; }
.range-words { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 10px; }
.range-words p { margin: 0; font-family: var(--cd-serif); font-size: clamp(1.2rem, 2.6vw, 1.7rem); color: #2f2618; text-shadow: 0 2px 18px rgba(247, 240, 224, 0.96), 0 0 4px rgba(247, 240, 224, 0.9); }
.range-words a { color: #a8431f; font-weight: 700; text-shadow: 0 2px 14px rgba(247, 240, 224, 0.96); }

@media (prefers-reduced-motion: reduce) {
  .art-medal, .epigraph, .lead, .actions, .scroll-cue { animation: none !important; opacity: 1 !important; }
  .reveal { opacity: 1; transform: none; transition: none; }
}
@media (max-width: 820px) { .forms { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 520px) { .forms { grid-template-columns: 1fr; } .forms-sec { padding: 60px 20px 40px; } }
</style>
