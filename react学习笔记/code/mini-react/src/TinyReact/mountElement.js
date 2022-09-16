import mountNativeElement from './mountNativeElement'

export default function mountComponent(virtualDom,container){
  // 类组件  函数组件
  mountNativeElement(virtualDom,container)
}