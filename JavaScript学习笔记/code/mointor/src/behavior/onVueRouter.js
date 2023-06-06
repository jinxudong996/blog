import { addCache } from '../cache/cache'
import { getUUID } from './utils'
import { getPageURL } from '../util'

export default function onVueRouter(router) {
  router.beforeEach((to, from, next) => {
    // 首次加载页面不用统计
    if (!from.name) {
      return next()
    }

    const data = {
      params: to.params,
      query: to.query,
    }

    addCache({
      data,
      name: to.name || to.path,
      type: 'behavior',
      subType: ['vue-router-change', 'pv'],
      startTime: performance.now(),
      from: from.fullPath,
      to: to.fullPath,
      uuid: getUUID(),
    })

    next()
  })
}