import { isSupportSendBeacon } from "./util"
import config from './config'

const sendBeacon = isSupportSendBeacon() ? window.navigator.sendBeacon.bind(window.navigator) : reportWithIMG

export report(data){
  const reportData = JSON.stringify({
    id: sessionID,
    appID: config.appID,
    userID: config.userID,
    data,
  })
  if (window.requestIdleCallback) {
    window.requestIdleCallback(() => {
      sendBeacon(config.url, reportData)
    }, { timeout: 3000 })
  } else {
    setTimeout(() => {
      sendBeacon(config.url, reportData)
    })
  }


}

reportWithIMG(url,data){
  var img = new Image();
  img.width = 1;
  img.height = 1;
  let str = '?'
  for(let item in data){
    str += item + '=' + data[item] + '&'
  }
  img.src = url + str
  console.log('准备发送', img.src)
}