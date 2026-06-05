import { defineConfig } from 'vitepress'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

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

// 侧栏与顶部导航：由 tools/split_build.py 生成（单一事实来源；加新份不用改这里）
const navSidebar = JSON.parse(
  readFileSync(fileURLToPath(new URL('./sidebars.json', import.meta.url)), 'utf-8'),
) as { sidebars: Record<string, unknown>; nav: unknown[] }

export default defineConfig({
  lang: 'zh-CN',
  title: '内功',
  description: '招式人人会，内功定高下。vibe coding 时代，懂底层原理是你压住模型、决定上限的内功。',
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
    nav: [{ text: '首页', link: '/' }, ...(navSidebar.nav as any[])],
    sidebar: navSidebar.sidebars as any,
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
      message: '招式人人会，内功定高下',
      copyright: '计算机底层 · vibe coding 时代的内功 · 持续增加',
    },
  },
  markdown: {
    config: (md) => md.use(calloutPlugin),
    lineNumbers: false,
    image: { lazyLoading: true },
  },
})
