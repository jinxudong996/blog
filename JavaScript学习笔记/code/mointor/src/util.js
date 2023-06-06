export function onBeforeunload(callback) {
  window.addEventListener('beforeunload', callback, true)
}

export function onHidden(callback, once) {
  const onHiddenOrPageHide = (event) => {
      if (event.type === 'pagehide' || document.visibilityState === 'hidden') {
          callback(event)
          // if (once) {
          //     window.removeEventListener('visibilitychange', onHiddenOrPageHide, true)
          //     window.removeEventListener('pagehide', onHiddenOrPageHide, true)
          // }
      }
  }
  window.addEventListener('visibilitychange', onHiddenOrPageHide, true)
  window.addEventListener('pagehide', onHiddenOrPageHide, true)
}

export function isSupportSendBeacon() {
  return !!window.navigator?.sendBeacon
}

export default function generateUniqueID() {
  return `v2-${Date.now()}-${Math.floor(Math.random() * (9e12 - 1)) + 1e12}`
}

export function getPageURL() {
  return window.location.href 
}

export function executeAfterLoad(callback) {
  if (document.readyState === 'complete') {
      callback()
  } else {
      const onLoad = () => {
          callback()
          window.removeEventListener('load', onLoad, true)
      }

      window.addEventListener('load', onLoad, true)
  }
}


