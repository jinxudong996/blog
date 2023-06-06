import { setConfig } from './config'
import { getCache, clearCache } from './cache/cache'
import { report } from './report'
import error from './error/index'
import behavior from './behavior'


const mointot = {
  init(options = {}) {
    setConfig(options)
    error()
    behavior()
    // 当页面进入后台或关闭前时，将所有的 cache 数据进行上报
    [onBeforeunload, onHidden].forEach(fn => {
      fn(() => {
        const data = getCache()
        if (data.length) {
          report(data, true)
          clearCache()
        }
      })
    })
  }
}