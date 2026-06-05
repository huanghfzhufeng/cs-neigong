<script setup lang="ts">
import { withBase } from 'vitepress'
import site from '../sidebars.json'

// 每份的一句话描述（按 slug）。加新份时在这里补一句即可；结构本身从 sidebars.json 自动同步。
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

// 从 sidebars.json 的导航自动构建分组卡片：新增一份会自动出现在首页
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

const chain = ['计算机网络', '操作系统', '互联网架构', 'MySQL']
</script>

<template>
  <div class="landing">
    <!-- Hero：内功 -->
    <section class="hero">
      <p class="kicker">计算机底层 · 图文详解</p>
      <h1>招式人人会，<br />内功定高下。</h1>
      <p class="sub">
        vibe coding 时代，模型什么都能做——做得好不好，看你的内功有多深。这套手册把计算机底层一份份讲透：是什么、为什么、解决什么、怎么用。
      </p>
      <p class="why">
        懂了底层，你才压得住模型，而不是把垃圾越堆越高。<br />
        人和模型相互成就，你的上限，决定它能帮你到哪。
      </p>
      <div class="actions">
        <a class="btn primary" :href="withBase('/00-导读')">从导读开始</a>
        <a class="btn ghost" :href="withBase('/01-计算机组成原理/')">随便翻一份</a>
      </div>
    </section>

    <!-- Hook：底层是一个整体 -->
    <section class="hook">
      <h2>底层不是一个个孤岛</h2>
      <p class="hook-lead">在浏览器敲下回车、到看见页面，这一瞬数据穿过了大半套手册：</p>
      <div class="chain">
        <template v-for="(c, i) in chain" :key="c">
          <span class="node">{{ c }}</span>
          <i v-if="i < chain.length - 1" class="arrow">→</i>
        </template>
      </div>
      <p class="hook-foot">
        底下垫着 <b>数据结构</b> 与 <b>计算机组成原理</b>。<a :href="withBase('/00-导读')">看这条线怎么串起一切 →</a>
      </p>
    </section>

    <!-- 目录：按内功的层次铺开 -->
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

    <!-- 怎么用这个站 -->
    <section class="howto">
      <h2>怎么用这个站</h2>
      <div class="hcols">
        <div class="hcol">
          <h4>通读</h4>
          <p>第一遍按顺序读，重点是每个“为什么”和每张图。</p>
        </div>
        <div class="hcol">
          <h4>速查</h4>
          <p>写代码时冒出疑问，右上角搜索（⌘K），秒级跳到那个点。</p>
        </div>
        <div class="hcol">
          <h4>炼内功</h4>
          <p>每章末「放到 vibe coding 里」把知识连到“怎么判断模型给的对不对”。</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.landing {
  max-width: 1060px;
  margin: 0 auto;
  padding: 0 28px 110px;
}

/* ---------- Hero ---------- */
.hero {
  padding: 92px 0 64px;
  border-bottom: 1px solid var(--cd-rule);
}
.kicker {
  margin: 0 0 22px;
  color: var(--vp-c-brand-1);
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.14em;
}
.hero h1 {
  margin: 0;
  font-family: var(--cd-serif);
  font-weight: 600;
  font-size: clamp(2.8rem, 6.5vw, 4.6rem);
  line-height: 1.06;
  letter-spacing: -0.01em;
  color: var(--vp-c-text-1);
}
.hero .sub {
  margin: 28px 0 0;
  max-width: 34em;
  font-size: 1.26rem;
  line-height: 1.55;
  color: var(--vp-c-text-1);
}
.hero .why {
  margin: 18px 0 0;
  max-width: 40em;
  font-size: 1.02rem;
  line-height: 1.75;
  color: var(--vp-c-text-2);
}
.actions {
  display: flex;
  gap: 14px;
  margin-top: 40px;
  flex-wrap: wrap;
}
.btn {
  display: inline-flex;
  align-items: center;
  padding: 11px 22px;
  border-radius: 999px;
  font-size: 0.98rem;
  font-weight: 600;
  transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
}
.btn.primary {
  background: var(--vp-c-brand-1);
  color: #fff;
}
.btn.primary:hover {
  background: var(--vp-c-brand-2);
  transform: translateY(-1px);
}
.btn.ghost {
  border: 1px solid var(--vp-c-border);
  color: var(--vp-c-text-1);
}
.btn.ghost:hover {
  border-color: var(--vp-c-brand-3);
  transform: translateY(-1px);
}

/* ---------- Hook ---------- */
.hook {
  padding: 60px 0;
  border-bottom: 1px solid var(--cd-rule);
}
.hook h2 {
  margin: 0;
  font-family: var(--cd-serif);
  font-size: 1.9rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.hook-lead {
  margin: 14px 0 26px;
  font-size: 1.08rem;
  color: var(--vp-c-text-2);
}
.chain {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px 14px;
}
.node {
  padding: 9px 18px;
  border-radius: 10px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 600;
  font-size: 1rem;
}
.arrow {
  color: var(--vp-c-text-3);
  font-style: normal;
  font-size: 1.1rem;
}
.hook-foot {
  margin: 26px 0 0;
  color: var(--vp-c-text-2);
}
.hook-foot b {
  color: var(--vp-c-text-1);
}
.hook-foot a {
  color: var(--vp-c-brand-1);
  font-weight: 600;
  white-space: nowrap;
}

/* ---------- 目录分组 ---------- */
.catalog {
  padding: 56px 0 20px;
}
.catalog-intro {
  margin: 0 0 26px;
  color: var(--vp-c-text-3);
  font-size: 0.95rem;
  letter-spacing: 0.02em;
}
.group {
  margin-bottom: 44px;
}
.group-head {
  display: flex;
  align-items: baseline;
  gap: 14px;
  margin-bottom: 18px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--cd-rule);
  flex-wrap: wrap;
}
.group-head h3 {
  margin: 0;
  font-family: var(--cd-serif);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.group-desc {
  font-size: 0.92rem;
  color: var(--vp-c-text-3);
}
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 16px;
}
.card {
  display: grid;
  grid-template-columns: auto 1fr;
  grid-template-rows: auto auto;
  column-gap: 16px;
  align-items: center;
  padding: 20px 22px;
  border: 1px solid var(--vp-c-border);
  border-radius: 14px;
  background: var(--vp-c-bg-elv);
  transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;
}
.card:hover {
  border-color: var(--vp-c-brand-3);
  transform: translateY(-3px);
  box-shadow: 0 10px 26px rgba(40, 30, 20, 0.09);
}
.card .no {
  grid-row: 1 / 3;
  font-family: var(--cd-serif);
  font-size: 2.1rem;
  font-weight: 600;
  color: var(--vp-c-brand-2);
  line-height: 1;
}
.card .ct {
  font-family: var(--cd-serif);
  font-size: 1.16rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.card .cd {
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}

/* ---------- 怎么用这个站 ---------- */
.howto {
  margin-top: 30px;
  padding: 44px 36px;
  border-radius: 16px;
  background: var(--vp-c-bg-soft);
}
.howto h2 {
  margin: 0 0 26px;
  font-family: var(--cd-serif);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.hcols {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 30px;
}
.hcol h4 {
  margin: 0 0 8px;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--vp-c-brand-1);
}
.hcol p {
  margin: 0;
  font-size: 0.96rem;
  line-height: 1.7;
  color: var(--vp-c-text-2);
}

@media (max-width: 640px) {
  .landing { padding: 0 20px 72px; }
  .hero { padding: 60px 0 44px; }
}
</style>
