import { defineConfig } from 'vitepress'

// 给「一句话讲透 / 放到 vibe coding 里」这类引用块打上 class，便于差异化样式。
const CALLOUTS: Record<string, string> = {
  '一句话讲透': 'cd-core',
  '放到 vibe coding 里': 'cd-vibe',
}
function calloutPlugin(md: any) {
  md.core.ruler.push('cd_callout', (state: any) => {
    const t = state.tokens
    for (let i = 0; i < t.length; i++) {
      if (t[i].type !== 'blockquote_open') continue
      const inline = t[i + 2]
      if (!inline || inline.type !== 'inline' || !inline.children) continue
      const k = inline.children.findIndex((c: any) => c.type === 'strong_open')
      if (k < 0) continue
      const label = (inline.children[k + 1]?.content || '').trim()
      const cls = CALLOUTS[label]
      if (cls) t[i].attrJoin('class', cls)
    }
    return true
  })
}

// 单一事实来源：文件名 → 侧栏/导航标题
const ORDER: [string, string][] = [
  ['00-导读', '导读 · 把九份连成一张网'],
  ['01-计算机组成原理', '01 · 计算机组成原理'],
  ['02-操作系统', '02 · 操作系统'],
  ['03-计算机网络', '03 · 计算机网络'],
  ['04-数据结构与算法', '04 · 数据结构与算法'],
  ['05-MySQL', '05 · MySQL'],
  ['06-互联网架构演进', '06 · 互联网架构演进'],
  ['07-系统质量属性与架构评估', '07 · 系统质量属性与架构评估'],
  ['08-软件工程', '08 · 软件工程'],
  ['09-LLM与Agent工程', '09 · LLM 与 Agent 工程'],
]

export default defineConfig({
  lang: 'zh-CN',
  title: '计算机基础 · 真懂手册',
  description: '不是为了面试，是为了真懂——是什么、为什么、解决什么、怎么用。懂了这些，vibe coding 时你才压得住模型。',
  base: '/cs-neigong/',
  srcExclude: ['README.md'],
  ignoreDeadLinks: true,
  lastUpdated: true,
  metaChunk: true,
  head: [
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap' }],
    ['meta', { name: 'theme-color', content: '#c2603f' }],
  ],
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '导读', link: '/00-导读' },
      { text: '九份详解', items: ORDER.slice(1).map(([f, t]) => ({ text: t, link: `/${f}` })) },
    ],
    sidebar: [
      {
        text: '计算机基础 · 真懂手册',
        items: ORDER.map(([f, t]) => ({ text: t, link: `/${f}` })),
      },
    ],
    outline: { level: [2, 3], label: '本页章节' },
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索内容', buttonAriaLabel: '搜索内容' },
          modal: {
            displayDetails: '显示详细列表',
            resetButtonTitle: '清除查询',
            backButtonTitle: '返回',
            noResultsText: '没有找到相关结果',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },
    docFooter: { prev: '上一篇', next: '下一篇' },
    sidebarMenuLabel: '目录',
    returnToTopLabel: '回到顶部',
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
    lastUpdatedText: '最后更新于',
    socialLinks: [{ icon: 'github', link: 'https://github.com/huanghfzhufeng/cs-neigong' }],
    footer: {
      message: '为真懂而做 · 不是为了面试',
      copyright: '内容为个人学习笔记，持续打磨',
    },
  },
  markdown: {
    config: (md) => md.use(calloutPlugin),
    lineNumbers: false,
    image: { lazyLoading: true },
  },
})
