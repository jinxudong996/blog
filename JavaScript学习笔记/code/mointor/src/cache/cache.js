import {report} from '../report'

let cache = []
let bigNum = 50

export function addCache(data){
  if(cache.length > bigNum){
    // 这里有问题 分别出data的格式 对象和数组
    report(cache)
  }else{
    cache.unshift(data)
  }
}

export function getCache(data){
  return cache
}

export function clearCache(data){
  cache = []
}
