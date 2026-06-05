<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import { useData, useRoute } from 'vitepress'

const { isDark } = useData()
const route = useRoute()
const container = ref<HTMLElement>()
const theme = () => (isDark.value ? 'transparent_dark' : 'light')

function render() {
  const el = container.value
  if (!el) return
  el.innerHTML = ''
  const s = document.createElement('script')
  s.src = 'https://giscus.app/client.js'
  s.async = true
  s.crossOrigin = 'anonymous'
  const attrs: Record<string, string> = {
    'data-repo': 'huanghfzhufeng/cs-neigong',
    'data-repo-id': 'R_kgDOSxl4RQ',
    'data-category': 'Announcements',
    'data-category-id': 'DIC_kwDOSxl4Rc4C-kIk',
    'data-mapping': 'pathname',
    'data-strict': '0',
    'data-reactions-enabled': '1',
    'data-emit-metadata': '0',
    'data-input-position': 'top',
    'data-theme': theme(),
    'data-lang': 'zh-CN',
    'data-loading': 'lazy',
  }
  for (const [k, v] of Object.entries(attrs)) s.setAttribute(k, v)
  el.appendChild(s)
}

function syncTheme() {
  const iframe = document.querySelector<HTMLIFrameElement>('iframe.giscus-frame')
  iframe?.contentWindow?.postMessage(
    { giscus: { setConfig: { theme: theme() } } },
    'https://giscus.app',
  )
}

onMounted(() => nextTick(render))
watch(() => route.path, () => nextTick(render))
watch(isDark, syncTheme)
</script>

<template>
  <div class="cd-comments">
    <h2 class="cd-comments-title">切磋 · 评论</h2>
    <p class="cd-comments-hint">用 GitHub 账号登录即可留言、提问、打卡。</p>
    <div ref="container" class="cd-giscus"></div>
  </div>
</template>

<style scoped>
.cd-comments { margin-top: 56px; padding-top: 30px; border-top: 1px solid var(--cd-rule); }
.cd-comments-title { font-family: var(--cd-serif); font-size: 1.35rem; font-weight: 600; margin: 0; color: var(--vp-c-text-1); letter-spacing: 0.04em; }
.cd-comments-hint { margin: 8px 0 18px; font-size: 0.9rem; color: var(--vp-c-text-3); }
.cd-giscus { min-height: 160px; }
</style>
