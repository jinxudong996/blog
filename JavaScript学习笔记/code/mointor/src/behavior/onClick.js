import { addCache } from '../cache/cache'
import { getUUID } from './utils'
import { getPageURL } from '../util'

export default function onClick() {
  ['mousedown', 'touchstart'].forEach(eventType => {
    let timer
    window.addEventListener(eventType, event => {
      clearTimeout(timer)
      timer = setTimeout(() => {
        const target = event.target
        const { top, left } = target.getBoundingClientRect()

        addCache({
          top,
          left,
          eventType,
          pageHeight: document.documentElement.scrollHeight || document.body.scrollHeight,
          scrollTop: document.documentElement.scrollTop || document.body.scrollTop,
          type: 'behavior',
          subType: 'click',
          target: target.tagName,
          paths: event.path?.map(item => item.tagName).filter(Boolean),
          startTime: event.timeStamp,
          pageURL: getPageURL(),
          outerHTML: target.outerHTML,
          innerHTML: target.innerHTML,
          width: target.offsetWidth,
          height: target.offsetHeight,
          viewport: {
            width: window.innerWidth,
            height: window.innerHeight,
          },
          uuid: getUUID(),
        })
      }, 500)
    })
  })
}