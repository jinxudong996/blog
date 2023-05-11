import {report} from './report'

let cache = []
let bigNum = 5000

export function addCache(data){
  if(cache.length > 5000){
    // 这里有问题 分别出data的格式 对象和数组
    report(cache)
  }else{
    cache.unshift(data)
  }
}