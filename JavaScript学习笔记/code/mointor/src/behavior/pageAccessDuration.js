import { addCache } from '../cache/cache'
import { onBeforeunload, getPageURL } from '../util'
import { getUUID } from './utils'

export default function pageAccessDuration() {
  onBeforeunload(() => {
    addCache({
      type: 'behavior',
      subType: 'page-access-duration',
      startTime: performance.now(),
      pageURL: getPageURL(),
      uuid: getUUID(),
    }, true)
  })
}