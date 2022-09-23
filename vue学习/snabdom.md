#### snabbdom基本用法

Snabbdom 是一个专注于简单性、模块化、强大特性和性能的虚拟 DOM 库。其中有几个核心特性：

1. 核心代码 200 行，并且提供丰富的测试用例；
2. 拥有强大模块系统，并且支持模块拓展和灵活组合；
3. 在每个 VNode 和全局模块上，都有丰富的钩子，可以在 Diff 和 Patch 阶段使

接下来通过实例更加直观的认识这个库。

##### 

##### 基本用法

首先新建一个项目，对项目进行初始化`npm init -y`，安装模块`npm install snabbdom`，新建`index.html`，设置入口元素：`<div id="app"></div>`，再新建`src/01-basicusage.js`，在这个文件中写入我们的示例代码：

```javascript
import { init } from 'snabbdom/build/package/init'
import { h } from 'snabbdom/build/package/h'

const patch = init([])
let vnode = h('div#app', 'Hello world1')
const app = document.getElementById('app')
patch(app, vnode)
```

这里首先导入两个函数`init`和`h`，其中`init`  需要一个模块列表并返回一个`patch`使用指定模块集的函数 ，而patch方法就是对比两个虚拟dom，将差异更新到视图中，h方法生产虚拟dom，h方法接受两个参数，第一个参数标签加选择器，第二个参数就是我们的文本。在上述例子中，patch第一个参数是一个dom节点，patch方法会在内部将其转化为虚拟dom，并将差异部分更新到页面中。



##### 模块

Snabbdom 的核心库并不能处理DOM 元素的属性/样式/事件等，可以通过注册 Snabbdom 默认提供的模块来实现，也可以用来扩展Snabbdom的功能。Snabbdom 中的模块的实现是通过注册全局的钩子函数来实现的 。

官网提供了六个模块

- attributes，设置属性，内部使用的setAttribute方法实现的
- props，也是设置属性的，通过obj.prop来设置的，不支持布尔值
- dataset  处理html5中的data-属性的
- style  切换样式
- class  设置行内样式
- eventlisteners  注册事件

模块的使用有以下三个步骤：

- 导入所需模块
- init()注册模块
- h()函数的第二个参数处使用模块

接下来写一个简单的例子：

根据上述步骤，首先导入所需模块：

```javascript
import { styleModule } from 'snabbdom/build/package/modules/style'
import { eventListenersModule } from 'snabbdom/build/package/modules/eventlisteners'
```

注册模块：

```javascript
const patch = init([
  styleModule,
  eventListenersModule
])
```

使用h() 函数的第二个参数传入模块中使用的数据（对象）：

```javascript
let vnode = h('div', [
  h('h1', { style: { backgroundColor: 'red' } }, 'Hello World'),
  h('p', { on: { click: eventHandler } }, 'Hello P')
])

function eventHandler () {
  console.log('aaa')
}
```

最后调用patch函数对比差异渲染到页面上：

```javascript
let app = document.querySelector('#app')
patch(app, vnode)
```



##### 源码解析

源码地址如下：https://github.com/snabbdom，这里安利一个chrome看源码的插件[octotree](https://github.com/ovity/octotree)，在git上看源码很方便。

###### h函数

h函数在上面的例子中已经使用过了，作用就是返回一个虚拟dom。它的地址：https://github.com/snabbdom/snabbdom/blob/master/src/h.ts，这里来看下它具体的代码：

![1663846429166](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1663846429166.png)



这里定义了四个h函数，也就是ts的函数重载，根据函数不同的参数调用不同的函数，这里的做了很多对参数的判断，我们看最后一个：这里面b参数，就是我们定义子元素的数据，里面也包含着模块中的数据被存储到data中；c如果是数组的话就是虚拟dom，如果不是就是文本元素，本文元素就存放到text中，虚拟dom就存放到children中；最后遍历children，调用vnode()方法将children中的数据全部转化为虚拟dom，最后再返回一个vnode函数的调用：` return vnode(sel, data, children, text, undefined); `

###### vnode函数

代码位置：https://github.com/snabbdom/snabbdom/blob/master/src/vnode.ts，这个函数比较简单的，

```javascript
export function vnode(
  sel: string | undefined,
  data: any | undefined,
  children: Array<VNode | string> | undefined,
  text: string | undefined,
  elm: Element | DocumentFragment | Text | undefined
): VNode {
  const key = data === undefined ? undefined : data.key;
  return { sel, data, children, text, elm, key };
}
```

就是反悔了一个对象，对象里的sel为选择器；data就是前面h函数的第二个参数，也就是模块中的数据；children和text是互斥的，只有一个生效，如果h函数第三个参数传的是字符串，那就是text，如果h函数第三个参数传的是vnode，那就是children生效；ele会存储当前vnode转换之后的dom元素；我们的k就被存放到data中了。

###### init函数

代码地址：https://github.com/snabbdom/snabbdom/blob/master/src/init.ts。

init函数在上述的例子中传入了两个模块来使用的，接下来看下内部的实现：

函数首先初始化了两个变量cbs和 api。 cbs 是一个有钩子函数名称组成的数组，api就是定义了dom操作的各个方法，接下来就两个for循环：

```javascript
//107行
for (const hook of hooks) {
    for (const module of modules) {
      const currentHook = module[hook];
      if (currentHook !== undefined) {
        (cbs[hook] as any[]).push(currentHook);
      }
    }
  }
```

首先遍历hooks，这个hooks就是顶一个钩子函数名称的数组，modules就是调用init函数传入的模块数组，比如前面一个例子：

```javascript
const patch = init([
  styleModule,
  eventListenersModule
])
```

实际上这个双循环就是将模块中的钩子函数存放到cbs数组中对应的钩子函数。

在最后返回了一个patch方法。

###### patch函数

这个path函数就是这个库的核心了，patch函数接受两个参数，分别是新旧vnode，通过对比新旧节点的变化来更新视图，也就是diff算法。然后返回一个新节点当做下次处理的旧节点。接下来看下这个函数的具体实现，代码位置：https://github.com/snabbdom/snabbdom/blob/master/src/init.ts#L428

首先从cbs中取出钩子函数，执行里面的pre()钩子函数，然后判断下oldVnode是不是vnode对象，如果不是的话调用 emptyNodeAt 将其转化为vndoe；然后再通过` sameVnode(oldVnode, vnode) `比对下oldVnode和vnode是否是相同类型的节点，如果是的话就直接调用` patchVnode(oldVnode, vnode, insertedVnodeQueue); `进行比对，如果不是，首先获取oldVnode的父节点，将新节点插入到父节点中，同时删除老节点。这里使用了三个复杂的函数  patchVnode、 createElm 和  removeVnodes ，接下来分别详细的看下：

- patchVnode

  代码位置：https://github.com/snabbdom/snabbdom/blob/3be76a428b4b627fb845f94534355a186bc11231/src/init.ts#L387。

  这里也主要分为三个步骤，首先触发prepatch和update钩子函数；随后开始比对vnode的差异，核心代码就是这里：

  ```javascript
  if (isUndef(vnode.text)) {
        if (isDef(oldCh) && isDef(ch)) {
          if (oldCh !== ch) updateChildren(elm, oldCh, ch, insertedVnodeQueue);
        } else if (isDef(ch)) {
          if (isDef(oldVnode.text)) api.setTextContent(elm, "");
          addVnodes(elm, null, ch, 0, ch.length - 1, insertedVnodeQueue);
        } else if (isDef(oldCh)) {
          removeVnodes(elm, oldCh, 0, oldCh.length - 1);
        } else if (isDef(oldVnode.text)) {
          api.setTextContent(elm, "");
        }
      } else if (oldVnode.text !== vnode.text) {
        if (isDef(oldCh)) {
          removeVnodes(elm, oldCh, 0, oldCh.length - 1);
        }
        api.setTextContent(elm, vnode.text!);
  }
  ```

  这里先判断是否有text属性，如果有就判断两个text是否相同，如果不相同直接删除旧节点，然后直接将text更新到对应的节点上；如果没有text属性，首先判断新旧节点是否都有子节点，而且不相同，调用updateChildren方法，在这个方法中对比所有的子节点并且更新dom；如果新节点和旧节点只有一个有子节点的话，也比较简单了，直接删除旧节点的内容，插入新节点的内容。最后触发钩子函数` hook?.postpatch?.(oldVnode, vnode); `

  这里在看下updateChildren方法，这个方法整个diff算法的核心。

  # 休息会，待会在看



- createElm

  这个方法主要是将vnode节点转化为对应的node元素，这个方法的代码在这里：https://github.com/snabbdom/snabbdom/blob/3be76a428b4b627fb845f94534355a186bc11231/src/init.ts#L146。

  这个方法主要分了三个步骤，首先执行用户设置的init钩子函数，

  ```javascript
  //148
  let data = vnode.data;
  if (data !== undefined) {
        const init = data.hook?.init;
        if (isDef(init)) {
          init(vnode);
          data = vnode.data;
        }
  }
  ```

  这里拿到数据中的传入的init方法，然后再执行，主要作用就是让用户在创建真实的dom之前可以更改vnode。接下来就将vnode渲染成真实的dom元素，这里并没有渲染到页面上，这里代码也都比较简单，根据sel的类型来创建不同的节点类型。最后将新创建的dom元素返回。将dom元素插入到页面上是在patch方法中的这行代码：` api.insertBefore(parent, vnode.elm!, api.nextSibling(elm)); `

- removeVnodes 

  这个函数是在452行调用的：

  ```javascript
  removeVnodes(parent, [oldVnode], 0, 0);
  ```

  接受四个参数，父元素节点、要删除的vnode的数组和数组中要删除的vnode的位置。代码位置：https://github.com/snabbdom/snabbdom/blob/master/src/init.ts#L250

  这里对传入的数组进行遍历，对vnode节点首先进行筛选，如果是文本节点直接调用` api.removeChild `;

  如果是vnode节点，就先触发销毁的钩子函数，，再调用` createRmCb(ch.elm!, listeners) `，这个函数是一个高阶函数，钩子函数都执行完毕后调用` api.removeChild(parent, childElm); `

###### 123

