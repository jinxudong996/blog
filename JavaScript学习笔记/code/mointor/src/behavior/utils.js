// import { generateUniqueID } from '../util'

let uuid = ''

function generateUniqueID() {
  return `v2-${Date.now()}-${Math.floor(Math.random() * (9e12 - 1)) + 1e12}`
}

export function getUUID() {
    if (uuid) return uuid

    // 如果是手机 APP，可以调用原生方法或者设备唯一标识当成 uuid
    uuid = localStorage.getItem('uuid')
    if (uuid) return uuid

    uuid = generateUniqueID()
    localStorage.setItem('uuid', uuid)
    return uuid
}