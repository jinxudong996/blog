##### 前言

vue中实现双向绑定原理就是数据劫持和发布订阅模式

发布订阅模式就是定义了对象间的一种一对多的关系，让多个观察者对象同时监听某一个主题对象，当对象发生改变时，所有依赖于它的对象都将得到通知。

数据劫持就是利用JavaScript的访问器属性，当对对象的属性进行赋值时，Object.defineProperty就可以通过set()方法劫持到数据的变化，然后通知发布者去通知所有的观察者，观察者收到通知以后，就会更新视图。

##### 发布订阅模式

> 发布-订阅模式又叫观察者模式，它定义对象间的一对多的依赖关系，当一个对象的状态发生改变时，所有依赖它的对象都将得到通知。在js开发中，一般用事件模型来代替传统的发布-订阅模式。
>
> 发布订阅模式可以广泛的应用于异步编程模式，用于替代传递回调函数的方案。比如可以订阅ajax请求的error和succ等事件。在异步编程中使用发布-订阅模式，就无需过多关注对象在异步运行期间的内部状态，只需订阅事件发生点即可。
>
> 发布订阅模式可以取代对象之间硬编码的通知机制，一个对象不在显示的调用另一个对象的某个接口。这种模式让两个对象松耦合地联系在一起，虽然不清楚彼此的细节，但不影响他们之间的相互通信。

实现发布-订阅模式步骤

- 首先要指定谁充当发布者

- 然后给发布者添加一个缓存列表，用于存放回调函数以便通知订阅者

- 最后发布消息时，发布者遍历这个缓存列表，一次触发里面存放的订阅则回调函数

  ```javascript
  let salesOffices = {}  //定义发布者
  salesOffices.clientList = {}  //缓冲列表
  salesOffices.listen = function(key, fn) {
      //如果没有订阅过此类消息  就给该类消息创建一个缓存列表
      if(!this.clientList[key]) {  
          this.clientList[key] = []
      }
      this.clientList[key].push(fn)
  }
  
  salesOffices.trigger = function() {
      let key = Array.prototype.shift.call(arguments) //取出消息类型
      let fns = this.clientList[key]  //取出该消息对应的回调函数集合
  
      if(!fns || fns.length ==0) {
          return false
      }
  
      for(let i=0, fn; fn = fns[i++];){
          fn.apply(this, arguments)  //arguments是发布消息时附送的参数
      }
  }
  
  salesOffices.listen('squareMeter88', function(price) { //订阅
      console.log('价格= ' + price)
  })
  
  salesOffices.listen('squareMeter110', function(price) { //订阅
      console.log('价格= ' + price)
  })
  
  salesOffices.trigger('squareMeter88', 20000000)  //发布
  salesOffices.trigger('squareMeter110', 30000000)  //发布
  ```

  这里定义了一个salesOffices对象，对象上一个clientList充当缓存列表，存放对应的订阅事件，对象上 listen函数来订阅事件，一旦调用了listen函数，即开始订阅了某个事情，就将订阅函数存放至缓存列表，trigger函数就是发布函数，函数里根据传入的参数拿出缓冲列表里的订阅事件，再执行订阅事件。但是这里只能订阅salesOffices 类的事件，可以将功能提取出来，放在一个单独的对象里，设置一个通用的订阅发布功能。

  ```JavaScript
  let event = {
      clientList: [],
      listen: function(key, fn) {
          if(!this.clientList[key]){
              this.clientList[key] = []
          }
          this.clientList[key].push(fn)
      },
      trigger:function(key, fn) {
          let k = Array.prototype.shift.call(arguments) //取出消息类型
          let fns = this.clientList[k]  //取出该消息对应的回调函数集合
  
          if(!fns || fns.length ==0) {
              return false
          }
  
          for(let i=0, fn; fn = fns[i++];) {
              console.log(this)
              fn.apply(this, arguments)  //arguments是发布消息时附送的参数
          }
      }
  }
  
  let installEvent = function(obj) {
      for(let i in event){
          obj[i] = event[i]
      }
  }
  
  let sales = {} 
  installEvent(sales)
  console.log(sales)
  sales.listen('squareMeter89', function(price) {
      console.log('价格： ' + price)
  })
  sales.trigger('squareMeter89', 22222222) //价格： 22222222
  ```

  这里将发布订阅功能全部封装到了一个event对象里，在installEvent里通过for...in遍历event对象，将event对象上的属性全部绑定到新对象obj上，此时新对象已经拥有了event全部的属性和方法，随后就可以通过发布和订阅来实现相应的功能。

##### 数据劫持

vue2.0数据劫持用的是defineProperty方法

>  该方法允许精确地添加或修改对象的属性。通过赋值操作添加的普通属性是可枚举的，在枚举对象属性时会被枚举到（[`for...in`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/for...in) 或 [`Object.keys`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/keys)[ ](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys)方法），可以改变这些属性的值，也可以[`删除`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/delete)这些属性。这个方法允许修改默认的额外选项（或配置）。默认情况下，使用 `Object.defineProperty()` 添加的属性值是不可修改（immutable）的。 

```javascript
const object1 = {};

Object.defineProperty(object1, 'property1', {
  value: 42,
  writable: false
});

object1.property1 = 77;
// throws an error in strict mode

console.log(object1.property1);
// expected output: 42
```

详细用法可以查看mdn[文档](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty)

##### vue响应式

在实例化vue时，官网时这样写的

```JavaScript
var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!'
  }
})
```

接下来编写class类。

该类主要完成以下四个功能：

- 通过属性保存选项的数据
- 把data中的成员转换成getter和setter，注入到vue实例中
- 调用observer对象，监听数据的变化
- 调用compiler对象，解析指令和差值表达式

```javascript
class Vue {
  constructor (options) {
    // 1. 通过属性保存选项的数据
    this.$options = options || {}
    this.$data = options.data || {}
    this.$el = typeof options.el === 'string' ? document.querySelector(options.el) : options.el
    // 2. 把data中的成员转换成getter和setter，注入到vue实例中
    this._proxyData(this.$data)
    // 3. 调用observer对象，监听数据的变化
    new Observer(this.$data)
    // 4. 调用compiler对象，解析指令和差值表达式
    new Compiler(this)
  }
  _proxyData (data) {
    // 遍历data中的所有属性
    Object.keys(data).forEach(key => {
      // 把data的属性注入到vue实例中
      Object.defineProperty(this, key, {
        enumerable: true,
        configurable: true,
        get () {
          return data[key]
        },
        set (newValue) {
          if (newValue === data[key]) {
            return
          }
          data[key] = newValue
        }
      })
    })
  }
}
```

接下来开始编写Observer类，该类负责把data选项中的属性转换成响应式数据，同时如果数据发生了变化，得发送通知：

```javascript
class Observer {
    constructor (data) {
      this.walk(data)
    }
    walk (data) {
      // 1. 判断data是否是对象
      if (!data || typeof data !== 'object') {
        return
      }
      // 2. 遍历data对象的所有属性
      Object.keys(data).forEach(key => {
        this.defineReactive(data, key, data[key])
      })
    }
    defineReactive (obj, key, val) {
      let that = this
      // 如果val是对象，把val内部的属性转换成响应式数据
      this.walk(val)
      Object.defineProperty(obj, key, {
        enumerable: true,
        configurable: true,
        get () {
          return val
        },
        set (newValue) {
          if (newValue === val) {
            return
          }
          val = newValue
          that.walk(newValue)
        }
      })
    }
  }
```

接下来开始编写Compiler，该类负责编译模板、解析指令/插值表达式，负责页面的首次渲染，当数据发生变化后重新渲染视图。实际上也就是dom操作。

```javascript
class Compiler {
  constructor (vm) {
    this.el = vm.$el
    this.vm = vm
    this.compile(this.el)
  }
  // 编译模板，处理文本节点和元素节点
  compile (el) {
    let childNodes = el.childNodes
    Array.from(childNodes).forEach(node => {
      // 处理文本节点
      if (this.isTextNode(node)) {
        this.compileText(node)
      } else if (this.isElementNode(node)) {
        // 处理元素节点
        this.compileElement(node)
      }

      // 判断node节点，是否有子节点，如果有子节点，要递归调用compile
      if (node.childNodes && node.childNodes.length) {
        this.compile(node)
      }
    })
  }
  // 编译元素节点，处理指令
  compileElement (node) {
    // console.log(node.attributes)
    // 遍历所有的属性节点
    Array.from(node.attributes).forEach(attr => {
      // 判断是否是指令
      let attrName = attr.name
      if (this.isDirective(attrName)) {
        // v-text --> text
        attrName = attrName.substr(2)
        let key = attr.value
        this.update(node, key, attrName)
      }
    })
  }

  update (node, key, attrName) {
    let updateFn = this[attrName + 'Updater']
    updateFn && updateFn.call(this, node, this.vm[key], key)
  }

  // 处理 v-text 指令
  textUpdater (node, value, key) {
    node.textContent = value
    new Watcher(this.vm, key, (newValue) => {
      node.textContent = newValue
    })
  }
  // v-model
  modelUpdater (node, value, key) {
    node.value = value
    new Watcher(this.vm, key, (newValue) => {
      node.value = newValue
    })
    // 双向绑定
    node.addEventListener('input', () => {
      this.vm[key] = node.value
    })
  }

  // 编译文本节点，处理差值表达式
  compileText (node) {
    // console.dir(node)
    // {{  msg }}
    let reg = /\{\{(.+?)\}\}/
    let value = node.textContent
    if (reg.test(value)) {
      let key = RegExp.$1.trim()
      node.textContent = value.replace(reg, this.vm[key])

      // 创建watcher对象，当数据改变更新视图
      new Watcher(this.vm, key, (newValue) => {
        node.textContent = newValue
      })
    }
  }
  // 判断元素属性是否是指令
  isDirective (attrName) {
    return attrName.startsWith('v-')
  }
  // 判断节点是否是文本节点
  isTextNode (node) {
    return node.nodeType === 3
  }
  // 判断节点是否是元素节点
  isElementNode (node) {
    return node.nodeType === 1
  }
}
```

紧接着要编写Dep类，在data的getter来搜集依赖，添加观察者，在setter中通知观察者。

```javascript
class Dep {
    constructor () {
      // 存储所有的观察者
      this.subs = []
    }
    // 添加观察者
    addSub (sub) {
      if (sub && sub.update) {
        this.subs.push(sub)
      }
    }
    // 发送通知
    notify () {
      this.subs.forEach(sub => {
        sub.update()
      })
    }
  }
```

 同时在Observer中搜集依赖、通知观察者： 

```javascript
get() {
    // 收集依赖
    Dep.target && dep.addSub(Dep.target)
    return val
},
set(newValue) {
    if (newValue === val) {
        return
    }
    val = newValue
    that.walk(newValue)
    // 发送通知
    dep.notify()
}
```

最后创建观察者watcher，当数据发生变化时触发依赖，dep通知所有的watcher实例更形势图，在自身实例化时往dep对象中添加自己。

```javascript
class Watcher {
    constructor (vm, key, cb) {
      this.vm = vm
      // data中的属性名称
      this.key = key
      // 回调函数负责更新视图
      this.cb = cb
  
      // 把watcher对象记录到Dep类的静态属性target
      Dep.target = this
      // 触发get方法，在get方法中会调用addSub
      this.oldValue = vm[key]
      Dep.target = null
    }
    // 当数据发生变化的时候更新视图
    update () {
      let newValue = this.vm[this.key]
      if (this.oldValue === newValue) {
        return
      }
      this.cb(newValue)
    }
  }
```

编写一个html文件进行验证：

```html
<!DOCTYPE html>
<html lang="cn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Mini Vue</title>
</head>
<body>
  <div id="app">
    <h1>差值表达式</h1>
    <h3>{{ msg }}</h3>
    <h3>{{ count }}</h3>
    <h1>v-text</h1>
    <div v-text="msg"></div>
    <h1>v-model</h1>
    <input type="text" v-model="msg">
    <input type="text" v-model="count">
  </div>
  <script src="./js/dep.js"></script>
  <script src="./js/watcher.js"></script>
  <script src="./js/compiler.js"></script>
  <script src="./js/observer.js"></script>
  <script src="./js/vue.js"></script>
  <script>
    let vm = new Vue({
      el: '#app',
      data: {
        msg: 'Hello Vue',
        count: 100,
        person: { name: 'zs' }
      }
    })
    console.log(vm.msg)
    // vm.msg = { test: 'Hello' }
    vm.test = 'abc'
  </script>
</body>
</html>
```

可以看到我们的差值表达式、双向绑定功能皆以完善。

