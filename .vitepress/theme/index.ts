import DefaultTheme from 'vitepress/theme'
import type { App } from 'vue'
import { onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vitepress'
import mediumZoom from 'medium-zoom'
import Landing from './Landing.vue'
import Layout from './Layout.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }: { app: App }) {
    app.component('Landing', Landing)
  },
  setup() {
    const route = useRoute()
    let zoom: ReturnType<typeof mediumZoom> | undefined
    const attach = () => {
      zoom?.detach()
      zoom = mediumZoom('.vp-doc img', {
        background: 'var(--cd-zoom-bg)',
        margin: 28,
      })
    }
    onMounted(() => nextTick(attach))
    watch(
      () => route.path,
      () => nextTick(attach),
    )
  },
}
