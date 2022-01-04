class Element{
  constructor(tagName, props, children){
    this.tagName = tagName
    this.props = props
    this.children = children
  }
  render(){
    let el = document.createElement(this.tagName) // 根据tagName构建
    let props = this.props
    for (let propName in props) { // 设置节点的DOM属性
      let propValue = props[propName]
      el.setAttribute(propName, propValue)
    }

    let children = this.children || []

    children.forEach( child => {
      let childEl = (child instanceof Element)
        ? child.render() // 如果子节点也是虚拟DOM，递归构建DOM节点
        : document.createTextNode(child) // 如果字符串，只构建文本节点
      el.appendChild(childEl)
    })

    return el
  }
}
