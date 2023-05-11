import { report } from './report'
import { addCache } from './addcache'
import { getPageURL } from './utils'

export default function error() {

  // 捕获资源加载失败错误 js css img...
  window.addEventListener('error', e => {
    const target = e.target
    if (!target) return

    if (target.src || target.href) {
      const url = target.src || target.href
      addCache({
        url,
        type: 'error',
        subType: 'resource',
        startTime: e.timeStamp,
        html: target.outerHTML,
        resourceType: target.tagName,
        paths: e.path.map(item => item.tagName).filter(Boolean),
        pageURL: getPageURL(),
      })
    }
  }, true)

  // 监听 js 错误
  window.onerror = (msg, url, line, column, error) => {
    addCache({
      msg,
      line,
      column,
      error: error.stack,
      subType: 'js',
      pageURL: url,
      type: 'error',
      startTime: performance.now(),
    })
  }

  // 监听 promise 错误 缺点是获取不到列数据
  window.addEventListener('unhandledrejection', e => {
    addCache({
      reason: e.reason?.stack,
      subType: 'promise',
      type: 'error',
      startTime: e.timeStamp,
      pageURL: getPageURL(),
    })
  })

  if (config.vue?.Vue) {
    config.vue.Vue.config.errorHandler = (err, vm, info) => {
      console.error(err)

      addCache({
        info,
        error: err.stack,
        subType: 'vue',
        type: 'error',
        startTime: performance.now(),
        pageURL: getPageURL(),
      })
    }
  }

}
