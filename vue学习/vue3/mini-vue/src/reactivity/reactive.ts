export function reactive(raw) {
  return new Proxy(raw, {
    get(target, key){

      // 搜集依赖
      const res = Reflect.get(target,key)
    },
    set(target, key, value){
      const res = Reflect.set(target,key,value)
      // 触发依赖
      return res
    }
  })
}