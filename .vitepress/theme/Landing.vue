<script setup lang="ts">
import { withBase } from 'vitepress'

const groups = [
  {
    title: '地基',
    desc: '机器与数据怎么运转——其余一切的底层支撑',
    items: [
      { no: '01', title: '计算机组成原理', desc: '机器到底怎么算：CPU、cache、内存、总线', link: '/01-计算机组成原理' },
      { no: '04', title: '数据结构与算法', desc: '数据怎么存、问题怎么高效解', link: '/04-数据结构与算法' },
    ],
  },
  {
    title: '运行与连接',
    desc: '程序怎么跑、请求怎么到',
    items: [
      { no: '02', title: '操作系统', desc: '硬件与应用之间的资源管理者：进程、内存、I/O', link: '/02-操作系统' },
      { no: '03', title: '计算机网络', desc: '数据怎么跨机器送达：TCP/IP、HTTP、HTTPS', link: '/03-计算机网络' },
    ],
  },
  {
    title: '数据与架构',
    desc: '怎么可靠存取、怎么扛住流量',
    items: [
      { no: '05', title: 'MySQL', desc: '索引、事务、锁、日志', link: '/05-MySQL' },
      { no: '06', title: '互联网架构演进', desc: '从单机到分布式，一步步扛住流量', link: '/06-互联网架构演进' },
    ],
  },
  {
    title: '方法与上层',
    desc: '怎么把事做对、怎么用好模型',
    items: [
      { no: '07', title: '系统质量属性与架构评估', desc: '用“质量属性”的语言谈架构与权衡', link: '/07-系统质量属性与架构评估' },
      { no: '08', title: '软件工程', desc: '把事做对、做稳的方法论', link: '/08-软件工程' },
      { no: '09', title: 'LLM 与 Agent 工程', desc: '怎么用模型把活干好——元能力', link: '/09-LLM与Agent工程' },
    ],
  },
]

const chain = ['计算机网络', '操作系统', '互联网架构', 'MySQL']
</script>

<template>
  <div class="landing">
    <!-- Hero -->
    <section class="hero">
      <p class="kicker">计算机基础 · 图文详解</p>
      <h1>不为面试，<br />为真懂。</h1>
      <p class="sub">九份图文详解，把计算机基础讲透——是什么、为什么、解决什么、怎么用。</p>
      <p class="why">
        懂了这些，vibe coding 时你才压得住模型，而不是把垃圾越堆越高。<br />
        人和模型是相互的，你的上限决定它能帮你到哪。
      </p>
      <div class="actions">
        <a class="btn primary" :href="withBase('/00-导读')">从导读开始</a>
        <a class="btn ghost" :href="withBase('/01-计算机组成原理')">随便翻一份</a>
      </div>
    </section>

    <!-- Hook：九份是一个整体 -->
    <section class="hook">
      <h2>九份不是九个孤岛</h2>
      <p class="hook-lead">在浏览器敲下回车、到看见页面，这一瞬数据穿过了大半本手册：</p>
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

    <!-- 九份，按学习路径分组 -->
    <section class="catalog">
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
          <h4>当手册</h4>
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
  line-height: 1.04;
  letter-spacing: -0.01em;
  color: var(--vp-c-text-1);
}
.hero .sub {
  margin: 28px 0 0;
  max-width: 30em;
  font-size: 1.32rem;
  line-height: 1.5;
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
