#### DOM解析流程

##### DOM是什么

从网络传给渲染引擎的HTML文件字节流是无法直接被渲染引擎理解的，所以要将其转化为渲染引擎能够理解的内部结构，这个结构就是DOM。DOM提供了对HTML文档结构化的表述，可以从三个方面来解释：

- 从页面的视角来看，DOM是生成页面的基础数据结构
- 从JavaScript脚本视角来看，DOM 提供给 JavaScript 脚本操作的接口，通过这套接口，JavaScript 可以对 DOM 结构进行访问，从而改变文档的结构、样式和内容 
-  从安全视角来看，DOM 是一道安全防护线，一些不安全的内容在 DOM 解析阶段就被拒之门外了 

##### DOM树如何生成

在渲染引擎内部，有一个叫`HTML解释器`的模块，它的职责就是负责将HTML字节流转换为DOM结构。

详细流程： 网络进程接收到响应头之后，会根据响应头中的 content-type 字段来判断文件的类型，比如 content-type 的值是“text/html”，那么浏览器就会判断这是一个 HTML 类型的文件，然后为该请求选择或者创建一个渲染进程。渲染进程准备好之后，网络进程和渲染进程之间会建立一个共享数据的管道，网络进程接收到数据后就往这个管道里面放，而渲染进程则从管道的另外一端不断地读取数据，并同时将读取的数据“喂”给 HTML 解析器。你可以把这个管道想象成一个“水管”，网络进程接收到的字节流像水一样倒进这个“水管”，而“水管”的另外一端是渲染进程的 HTML 解析器，它会动态接收字节流，并将其解析为 DOM 。

这里面的核心步骤就是将代码字节流转换为DOM树，这里主要分为两个阶段：

- 通过分词器将字节流转换为 Token，这里的Token分为Tag Token和文本Token，Tag Token实际上就是标签Token， 比如<body>就是 StartTag ，</body>就是EndTag

- 将Token解析为DOM节点，添加到DOM树中

  HTML 解析器维护了一个Token 栈结构，该 Token 栈主要用来计算节点之间的父子关系，在第一个阶段中生成的 Token 会被按照顺序压到这个栈中。具体的处理规则如下所示：

  - 如果压入到栈中的是StartTag Token，HTML 解析器会为该 Token 创建一个 DOM 节点，然后将该节点加入到 DOM 树中，它的父节点就是栈中相邻的那个元素生成的节点。
  - 如果分词器解析出来是文本 Token，那么会生成一个文本节点，然后将该节点加入到 DOM 树中，文本 Token 是不需要压入到栈中，它的父节点就是当前栈顶 Token 所对应的 DOM 节点。
  - 如果分词器解析出来的是EndTag 标签，比如是 EndTag div，HTML 解析器会查看 Token 栈顶的元素是否是 StarTag div，如果是，就将 StartTag div 从栈中弹出，表示该 div 元素解析完成。



#### 虚拟DOM

在我们调用document.body.appendChild(node)往 body 节点上添加一个元素，调用该 API 之后会引发一系列的连锁反应。首先渲染引擎会将 node 节点添加到 body 节点之上，然后触发样式计算、布局、绘制、栅格化、合成等任务，我们把这一过程称为重排。除了重排之外，还有可能引起重绘或者合成操作，形象地理解就是牵一发而动全身。另外，对于 DOM 的不当操作还有可能引发强制同步布局和布局抖动的问题，这些操作都会大大降低渲染效率。因此，对于 DOM 的操作我们时刻都需要非常小心谨慎。

而虚拟DOM就是将页面改变的内容应用到虚拟 DOM 上，而不是直接应用到 DOM 上，在虚拟 DOM 收集到足够的改变时，再把这些变化一次性应用到真实的 DOM 上 。

##### 虚拟DOM算法

用 JavaScript 对象表示 DOM 信息和结构，当状态变更的时候，重新渲染这个 JavaScript 的对象结构， 再用新渲染的对象树去和旧的树进行对比，记录这两棵树差异。记录下来的不同就是我们需要对页面真正的 DOM 操作，然后把它们应用在真正的 DOM 树上， 这个就是Virtual DOM算法。

可以概括为以下三个步骤：

- 用 JavaScript 对象结构表示 DOM 树的结构；然后用这个树构建一个真正的 DOM 树，插入文档中
- 当状态变更的时候，重新构造一棵新的对象树。然后用新的树和旧的树进行比较，记录两棵树差异
- 用差异构建真正的DOM树去更新视图

接下来根据三个步骤来实现下这个算法：

##### 用JavaScript对象模拟DOM树

首先写一段HTML代码实例：

```html
<ul id='list'>
  <li class='item'>Item 1</li>
  <li class='item'>Item 2</li>
  <li class='item'>Item 3</li>
</ul>
```

这段代码用JavaScript对象表示：

```javascript
var element = {
  tagName: 'ul', // 节点标签名
  props: { // DOM的属性，用一个对象存储键值对
    id: 'list'
  },
  children: [ // 该节点的子节点
    {tagName: 'li', props: {class: 'item'}, children: ["Item 1"]},
    {tagName: 'li', props: {class: 'item'}, children: ["Item 2"]},
    {tagName: 'li', props: {class: 'item'}, children: ["Item 3"]},
  ]
}
```

基于此我们创建一个element类：

```javascript
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

```

Element类的构造函数比较简单，就是将传入的标签名称、属性名称和子对象保存到实例中。

核心代码就是实例方法render方法。该方法首先根据传入的标签名称创建一个真正的标签，随后遍历传入的属性对象，使用setAttribute方法将属性对象中的键值对依次写入新创建的标签，最后再遍历传入的children对象，根据传入的children对象类型来递归创建文本节点和dom节点。

来验证下所创建的dom：

```javascript
var ul = new Element('ul', {id: 'list'}, [
    new Element('li', {class: 'item'}, ['Item 1']),
    new Element('li', {class: 'item'}, ['Item 2']),
    new Element('li', {class: 'item'}, ['Item 3'])
])
var ulRoot = ul.render()
document.body.appendChild(ulRoot)
```

可以看到页面中出现了我们创建的li标签。

##### 比较两颗虚拟DOM树的差异

比较两棵树的差异，正是 Virtual DOM 算法的核心的部分，也就是diff算法。在前段中，很少会跨层级的 移动DOM元素，Virtual DOM只会比较同一个层级。

![a](https://camo.githubusercontent.com/8589323ee9f10643f1c1e0b98b7676ca3a1e4d6c5ef29e99ff028d1dcbf9c5da/687474703a2f2f6c69766f7261732e6769746875622e696f2f626c6f672f7669727475616c2d646f6d2f636f6d706172652d696e2d6c6576656c2e706e67)

在遍历节点树进行比较时，每遍历到一个节点就把该节点和新的的树进行对比。如果有差异的话就记录到一个对象里面。 

差异一般就是我们对DOM的操作，主要包括：

- 替换原来的节点
- 移动、删除、新增子节点
- 修改节点属性
- 更改文本内容

根据上述差异定义几个常量，代表差异类型：

```javascript
var REPLACE = 0
var REORDER = 1
var PROPS = 2
var TEXT = 3
```

- 对于节点替换，可以直接判断节点的`tagName`，如果将`div`，`section`就记录：

  ```javascript
  patches[0] = [{
    type: REPALCE,
    node: newNode // el('section', props, children)
  }]
  ```

- 给`div`新增属性，记录为

  ```javascript
  patches[0] = [{
    type: REPALCE,
    node: newNode // el('section', props, children)
  }, {
    type: PROPS,
    props: {
      id: "container"
    }
  }]
  ```

- 文本节点更改

  ```javascript
  patches[2] = [{
    type: TEXT,
    content: "Virtual DOM2"
  }]
  ```

- 如果对节点进行增删查改，就比较复杂了。如果直接替换，DOM开销就很大了，实际上我们只要知道节点移动方式即可。比如旧节点顺序：a b c d e f g h i，新节点顺序：a b c h d f g i j。现在知道了新旧顺序，求最小的插入、删除操作，也就是字符串的最小编辑距离问题（力扣72）。我们将节点的操作记录为：

  ```javascript
  patches[0] = [{
    type: REORDER,
    moves: [{remove or insert}, {remove or insert}, ...]
  }]
  ```

这里核心部分关于diff的实现，还有点懵，暂做个记录，慢慢看。[原代码](https://github.com/livoras/list-diff)

##### 用差异构建真正的DOM树

有了的`patches`对象中找出当前遍历的节点差异，然后进行 DOM 操作 

```javascript
function applyPatches (node, currentPatches) {
  _.each(currentPatches, function (currentPatch) {
    switch (currentPatch.type) {
      case REPLACE:
        var newNode = (typeof currentPatch.node === 'string')
          ? document.createTextNode(currentPatch.node)
          : currentPatch.node.render()
        node.parentNode.replaceChild(newNode, node)
        break
      case REORDER:
        reorderChildren(node, currentPatch.moves)
        break
      case PROPS:
        setProps(node, currentPatch.props)
        break
      case TEXT:
        if (node.textContent) {
          node.textContent = currentPatch.content
        } else {
          // fuck ie
          node.nodeValue = currentPatch.content
        }
        break
      default:
        throw new Error('Unknown patch type ' + currentPatch.type)
    }
  })
}
```







