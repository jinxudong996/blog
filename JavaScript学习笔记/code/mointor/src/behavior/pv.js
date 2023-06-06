import { addCache } from '../cache/cache'
import { getUUID } from './utils'
import { getPageURL } from '../util'

export default function pv() {
  addCache({
    type: 'behavior',
    subType: 'pv',
    startTime: performance.now(),
    pageURL: getPageURL(),
    referrer: document.referrer,
    uuid: getUUID(),
  })
}