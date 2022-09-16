import mountElement from './mountElement'
import updateNodeElement from './updateNodeElement'

export default function createDOMElement(virtualDom){
  let newElement = null;
  if(virtualDom.type === 'text'){
    //文本节点
    newElement = document.createTextNode(virtualDom.props.textContent)
  }else{
    //元素节点
    newElement = document.createElement(virtualDom.type)
    updateNodeElement(newElement,virtualDom)
  }

  // 递归创建
  virtualDom.children.forEach(child => {
    mountElement(child,newElement)
  });
  return newElement
}