import { setConfig } from './config'
import { getCache, clearCache } from './util'
import { report } from './report'


const mointot = {
  init(options = {}){
    setConfig(options)

    // 当页面进入后台或关闭前时，将所有的 cache 数据进行上报
    [onBeforeunload, onHidden].forEach(fn => {
      fn(() => {
          // const data = getCache()
          // if (data.length) {
          //     report(data, true)
          //     clearCache()
          // }
          report(data, true)
      })
    })
  }
}