<script setup lang="ts">
import { withBase } from 'vitepress'
import { onMounted, onUnmounted, computed } from 'vue'
import site from '../sidebars.json'

const GH = 'https://github.com/huanghfzhufeng/cs-neigong'

// ---------- 宇宙 hero：九份化作环绕的行星 ----------
const RAW = [
  { no: '01', name: '计算机组成原理', link: '/01-计算机组成原理/', c1: '#f3b079', c2: '#c2603f', size: 80, ring: true },
  { no: '02', name: '操作系统', link: '/02-操作系统/', c1: '#79ddd0', c2: '#2f9e8f', size: 66, ring: false },
  { no: '03', name: '计算机网络', link: '/03-计算机网络/', c1: '#8cbcf2', c2: '#3b6fc2', size: 70, ring: false },
  { no: '04', name: '数据结构与算法', link: '/04-数据结构与算法/', c1: '#a9e08f', c2: '#4e9e6a', size: 86, ring: false },
  { no: '05', name: 'MySQL', link: '/05-MySQL/', c1: '#f3d27a', c2: '#d99a3f', size: 64, ring: true },
  { no: '06', name: '互联网架构演进', link: '/06-互联网架构演进/', c1: '#c1a6f3', c2: '#7a5ec2', size: 76, ring: true },
  { no: '07', name: '系统质量属性与架构评估', link: '/07-系统质量属性与架构评估/', c1: '#f3a6c0', c2: '#c25e80', size: 60, ring: false },
  { no: '08', name: '软件工程', link: '/08-软件工程/', c1: '#a8b4cc', c2: '#5e6e8f', size: 64, ring: false },
  { no: '09', name: 'LLM 与 Agent 工程', link: '/09-LLM与Agent工程/', c1: '#e0a0e8', c2: '#9e4ec2', size: 74, ring: false },
]
const planets = RAW.map((p, i) => {
  const a = ((i * 360) / RAW.length - 90) * (Math.PI / 180)
  const x = 50 + 38 * Math.cos(a)
  const y = 50 + 38 * Math.sin(a)
  return { ...p, x, y, above: y < 46 }
})

// ---------- 星空（确定性散布，避免随机不可复现）----------
const starsUrl = computed(() => {
  let c = ''
  for (let i = 0; i < 180; i++) {
    const rx = Math.sin(i * 12.9898) * 43758.5453
    const ry = Math.sin(i * 78.233) * 12543.1234
    const rr = Math.sin(i * 37.719) * 9123.77
    const x = (rx - Math.floor(rx)) * 1000
    const y = (ry - Math.floor(ry)) * 1000
    const r = 0.5 + (rr - Math.floor(rr)) * 1.7
    const o = (0.25 + (Math.abs(Math.sin(i * 5.3)) * 0.6)).toFixed(2)
    c += `<circle cx='${x.toFixed(1)}' cy='${y.toFixed(1)}' r='${r.toFixed(2)}' fill='white' opacity='${o}'/>`
  }
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='1000' height='1000' viewBox='0 0 1000 1000' preserveAspectRatio='xMidYMid slice'>${c}</svg>`
  return `url("data:image/svg+xml,${encodeURIComponent(svg)}")`
})

function ballStyle(p: any) {
  return {
    width: `${p.size}px`,
    height: `${p.size}px`,
    background: `radial-gradient(circle at 34% 30%, ${p.c1}, ${p.c2} 72%)`,
    boxShadow: `0 0 22px -4px ${p.c2}, inset -6px -8px 14px rgba(0,0,0,0.35)`,
  }
}

function scrollDown() {
  document.querySelector('.below')?.scrollIntoView({ behavior: 'smooth' })
}

// 首页隐藏 VitePress 默认导航，让宇宙 hero 全屏铺满
onMounted(() => document.documentElement.classList.add('cosmos-home'))
onUnmounted(() => document.documentElement.classList.remove('cosmos-home'))

// ---------- 下方目录：从 sidebars.json 自动构建 ----------
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
    <!-- ===== 宇宙 Hero（全屏 · 暗） ===== -->
    <section class="cosmos">
      <div class="stars" :style="{ backgroundImage: starsUrl }"></div>

      <div class="cos-top">
        <span class="wordmark">内功</span>
        <a class="gh" :href="GH" target="_blank" rel="noreferrer">GitHub</a>
      </div>

      <div class="stage">
        <div class="orbit orbit-1"></div>
        <div class="orbit orbit-2"></div>

        <!-- 中心：内功能量核 -->
        <div class="core">
          <div class="core-disc"></div>
          <div class="core-orb"></div>
          <div class="core-ring"></div>
        </div>

        <!-- 九大行星 -->
        <a
          v-for="p in planets"
          :key="p.no"
          class="planet"
          :class="{ above: p.above }"
          :style="{ left: p.x + '%', top: p.y + '%' }"
          :href="withBase(p.link)"
        >
          <span class="ball" :class="{ ringed: p.ring }" :style="ballStyle(p)"></span>
          <span class="plabel">{{ p.name }}</span>
        </a>
      </div>

      <div class="cos-foot">
        <p class="tagline">招式人人会，内功定高下 · vibe coding 时代的计算机底层</p>
        <div class="actions">
          <a class="btn primary" :href="withBase('/00-导读')">开始阅读</a>
          <a class="btn ghost" :href="GH" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </div>

      <button class="scroll-down" @click="scrollDown" aria-label="向下">↓</button>
    </section>

    <!-- ===== 下方内容（浅色） ===== -->
    <div class="below">
      <section class="hook">
        <h2>底层不是一个个孤岛</h2>
        <p class="hook-lead">在浏览器敲下回车、到看见页面，这一瞬数据穿过了大半套手册：</p>
        <div class="chain">
          <span class="node">计算机网络</span><i class="arrow">→</i>
          <span class="node">操作系统</span><i class="arrow">→</i>
          <span class="node">互联网架构</span><i class="arrow">→</i>
          <span class="node">MySQL</span>
        </div>
        <p class="hook-foot">
          底下垫着 <b>数据结构</b> 与 <b>计算机组成原理</b>。<a :href="withBase('/00-导读')">看这条线怎么串起一切 →</a>
        </p>
      </section>

      <section class="catalog">
        <p class="catalog-intro">按内功的层次铺开，持续增加：</p>
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
        <h2>怎么用这个站</h2>
        <div class="hcols">
          <div class="hcol"><h4>通读</h4><p>第一遍按顺序读，重点是每个“为什么”和每张图。</p></div>
          <div class="hcol"><h4>速查</h4><p>写代码时冒出疑问，搜索（⌘K）秒级跳到那个点。</p></div>
          <div class="hcol"><h4>炼内功</h4><p>每章末「放到 vibe coding 里」把知识连到“怎么判断模型给的对不对”。</p></div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
/* ===================== 宇宙 Hero ===================== */
.cosmos {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background:
    radial-gradient(ellipse 80% 70% at 50% 42%, #1b2540 0%, #0e1320 52%, #070810 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stars {
  position: absolute;
  inset: 0;
  background-size: cover;
  opacity: 0.9;
  pointer-events: none;
  animation: drift 180s linear infinite;
}
@keyframes drift { from { background-position: 0 0; } to { background-position: 0 -300px; } }

.cos-top {
  position: absolute;
  top: 22px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 34px;
  z-index: 5;
}
.wordmark {
  font-family: var(--cd-serif);
  font-size: 1.35rem;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.04em;
  text-shadow: 0 0 18px rgba(243, 176, 121, 0.5);
}
.gh {
  color: rgba(255, 255, 255, 0.72);
  font-size: 0.9rem;
  font-weight: 500;
}
.gh:hover { color: #fff; }

/* 行星舞台：正方形，随视口缩放 */
.stage {
  position: relative;
  width: min(86vw, 660px);
  height: min(86vw, 660px);
  margin: auto;
  flex: none;
}
.orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 50%;
}
.orbit-1 { width: 76%; height: 76%; }
.orbit-2 { width: 50%; height: 50%; border-color: rgba(255, 255, 255, 0.06); }

/* 中心能量核 */
.core {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 32%;
  height: 32%;
}
.core-orb {
  position: absolute;
  inset: 28%;
  border-radius: 50%;
  background: radial-gradient(circle at 50% 45%, #fff 0%, #ffe1b0 22%, #ef9a55 48%, rgba(204, 120, 92, 0) 74%);
  box-shadow: 0 0 70px 16px rgba(233, 150, 90, 0.4), 0 0 140px 40px rgba(204, 120, 92, 0.18);
  animation: pulse 5.5s ease-in-out infinite;
}
@keyframes pulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.06); opacity: 0.92; } }
.core-ring {
  position: absolute;
  inset: 6%;
  border-radius: 50%;
  border: 1px solid rgba(255, 220, 180, 0.28);
}
.core-disc {
  position: absolute;
  top: 64%;
  left: -8%;
  width: 116%;
  height: 46%;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 50%;
  transform: rotate(-12deg);
}

/* 行星 */
.planet {
  position: absolute;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  z-index: 3;
  text-decoration: none;
  transition: transform 0.2s ease;
}
.planet.above { flex-direction: column-reverse; }
.planet:hover { transform: translate(-50%, -50%) scale(1.08); z-index: 4; }
.ball {
  display: block;
  border-radius: 50%;
  position: relative;
}
.ball.ringed::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 168%;
  height: 46%;
  transform: translate(-50%, -50%) rotate(-22deg);
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 50%;
}
.plabel {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.92rem;
  font-weight: 500;
  white-space: nowrap;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.8);
}
.planet:hover .plabel { color: #fff; }

/* 底部文案 + 按钮 */
.cos-foot {
  position: relative;
  z-index: 5;
  text-align: center;
  padding-bottom: 64px;
}
.tagline {
  color: rgba(255, 255, 255, 0.78);
  font-size: 1.02rem;
  margin: 0 0 22px;
  letter-spacing: 0.02em;
}
.actions { display: flex; gap: 14px; justify-content: center; }
.btn {
  display: inline-flex;
  align-items: center;
  padding: 11px 26px;
  border-radius: 999px;
  font-size: 0.98rem;
  font-weight: 600;
  transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
}
.btn.primary { background: #c2603f; color: #fff; }
.btn.primary:hover { background: #d2724f; transform: translateY(-1px); }
.btn.ghost { border: 1px solid rgba(255, 255, 255, 0.28); color: #fff; }
.btn.ghost:hover { border-color: #fff; transform: translateY(-1px); }
.scroll-down {
  position: absolute;
  bottom: 22px;
  left: 50%;
  transform: translateX(-50%);
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  font-size: 1.4rem;
  cursor: pointer;
  animation: bob 2s ease-in-out infinite;
}
@keyframes bob { 0%, 100% { transform: translateX(-50%) translateY(0); } 50% { transform: translateX(-50%) translateY(6px); } }

/* ===================== 下方内容（浅色） ===================== */
.below { max-width: 1060px; margin: 0 auto; padding: 76px 28px 110px; }
.hook { padding-bottom: 50px; border-bottom: 1px solid var(--cd-rule); }
.hook h2 { margin: 0; font-family: var(--cd-serif); font-size: 1.9rem; font-weight: 600; color: var(--vp-c-text-1); }
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

@media (max-width: 720px) {
  .plabel { font-size: 0.74rem; }
  .below { padding: 56px 20px 72px; }
}
@media (max-width: 520px) {
  .plabel { display: none; }
  .stage { width: 92vw; height: 92vw; }
}
</style>
