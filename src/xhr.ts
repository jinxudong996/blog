import {AxiosRequestConfig} from './types'

export default function xhr(config:AxiosRequestConfig){
  const {data = null, url, method="get"} = config
  const request = new XMLHttpRequest()
  request.open(method.toUpperCase(), url , async:true)
  request.send(data)
}