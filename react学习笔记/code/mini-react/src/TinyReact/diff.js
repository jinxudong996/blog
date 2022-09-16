import mountElement from "./mountElement"

export default function diff(virtualDom,container,oldDOM){
  if(!oldDOM){
    mountElement(virtualDom,container)
  }
}