响应式系统学习笔记

#### 前言

vue3是采用Proxy来实现响应式数据的，之前写过一篇[博客](https://juejin.cn/post/7031371164911943711)总结过Proxy知识点，接下来回顾下：

> 使用代理的主要目的就是可以定义捕获器，而捕获器就是在处理程序中定义的基本操作拦截器。每个捕获器都对应一种基本操作，可以直接或间接在代理对象上使用。每次在代理对象上调用这些基本操作时，代理可以在这些操作传播到目标对象之前先调用捕获器函数，从而拦截并修改相应的行为。 

```javascript
const target = {
    id: 'target'
}

const handler = {
  get(){
    return 'no target'
  }
}
const proxy = new Proxy(target, handler)

proxy.id = 'foo'
console.log(target.id, proxy.id)
//foo no target
```

 当通过代理对象执行 get()操作时，就会触发定义的 get()捕获器 。 这里的get()被称之为捕获器 。

##### 初探响应式系统

响应式就是我们监控数据的变化，在数据发生更改时，自动执行响应的操作。

```html
<body></body>
<script>

const bucket = new Set()

// 原始数据
const data = { text: 'hello world' }
// 对原始数据的代理
const obj = new Proxy(data, {
  // 拦截读取操作
  get(target, key) {
    bucket.add(effect)
    // 返回属性值
    return target[key]
  },
  // 拦截设置操作
  set(target, key, newVal) {
    // 设置属性值
    target[key] = newVal
    bucket.forEach(fn => fn())
  }
})

function effect() {
  document.body.innerText = obj.text
}
effect()

</script>
```

这里就实现了一个简易的响应式，首先创建一个set结构存放操作函数，然后通过代理来监控原始数据data，当原始数据一旦有了属性读取操作，就讲操作函数放入set里面，一旦对原始数据进行了写操作，即对原始数据进行了修改，立马执行改操作。

写个定时器验证下：

```javascript
setTimeout(() => {
  obj.text = 'hello vue3'
}, 1000)
```

一秒钟后页面数据变成了`hello vue3`。

##### 完善响应式系统

然后这个响应式还是比较简陋的，我们硬编码将操作函数放到一个set里面，一旦操作函数名称发生了更改或者操作函数是个匿名函数，这个响应式系统立马就不能工作了，我们需要一个注册操作函数的机制（原文中将操作函数称之为副作用函数，set称之为桶，本菜鸡不喜欢，就不用了）。

```html
<body></body>
<script>

const bucket = new Set()

// 原始数据
const data = { text: 'hello world' }
// 对原始数据的代理
const obj = new Proxy(data, {
  // 拦截读取操作
  get(target, key) {
    if(activeEffect){
      bucket.add(activeEffect)
    }
    // 返回属性值
    return target[key]
  },
  // 拦截设置操作
  set(target, key, newVal) {
    // 设置属性值
    target[key] = newVal
    bucket.forEach(fn => fn())
  }
})

let activeEffect
function effect(fn) {
  activeEffect = fn
  fn()
}

effect(() => {
  console.log('effect run')
  document.body.innerText = obj.text
})

setTimeout(() => {
  obj.text = 'hello vue3'
}, 1000)

</script>
```

对响应式系统做了些优化，设置一个全局变量来存储操作函数，而effect也改成了接受一个函数，这样不管操作函数是什么名称，都不影响我们的响应式系统。

还有一个问题，如果我们在定时器中设置一个obj中不存在的属性，`obj.text1 = 'hello vue3`，会发现页面数据依然会更改，这就有问题了，响应式系统愿意是监控原始数据，而为原始数据添加属性也会触发我们的操作函数，这就有问题了。这里我们没有将操作函数与目标字段对应，无论操作哪个属性，都会执行一个操作函数。接下来需要将操作函数与目标字段一一对应起来。

用一个树状结构来将目标字段与操作函数对应起来

```
target
	---prop
		---fn
```

其中target表示监控对象，prop表示目标字段，fn表示操作函数，使用WeakMap来描述这一结构。之所以使用WeakMap而不是用map，WeakMap对于key是弱引用，不会影响垃圾回收机制工作，所以WeakMap特别适合存储那些只有当key所引用的对象存在时才有价值的信息，而map存储的信息，除非手动指定key为null，不然会一直存在的。

```javascript
const bucket = new WeakMap()
const obj = new Proxy(data, {
  // 拦截读取操作
  get(target, key) {
    // 将副作用函数 activeEffect 添加到存储副作用函数的桶中
    let depsMap = bucket.get(target)
    if (!depsMap) {
      bucket.set(target, (depsMap = new Map()))
    }
    let deps = depsMap.get(key)
    if (!deps) {
      depsMap.set(key, (deps = new Set()))
    }
    deps.add(activeEffect)

    // 返回属性值
    return target[key]
  },
  // 拦截设置操作
  set(target, key, newVal) {
    // 设置属性值
    target[key] = newVal
    // 把副作用函数从桶里取出并执行
    const depsMap = bucket.get(target)
    if (!depsMap) return
    const effects = depsMap.get(key)
    effects && effects.forEach(fn => fn())
  }
})
```

这里需要的WeakMap结构就是`WeakMap(targrt,map(prop,fn))`。代码里面首先从WeakMap里面取数据，如果不存在就新建一个目标字段和操作函数关联的map，这里的fn被放在一个set里面，不用数组是为了防止有重复的fn，最后将目标字段关联到一个map里。在监控数据时，依次从WeakMap里取map，从map里取操作函数，最后在依次执行操作函数。

最后再对代码进行下封装，将实现WeakMap结构的逻辑放到track函数里，触发操作函数的逻辑放到trigger里。

```html
<body></body>
<script>


const bucket = new WeakMap()

const data = { text: 'hello world' }
// 对原始数据的代理
const obj = new Proxy(data, {
  // 拦截读取操作
  get(target, key) {
    
    track(target, key)
    // 返回属性值
    return target[key]
  },
  // 拦截设置操作
  set(target, key, newVal) {
    // 设置属性值
    target[key] = newVal
   
    trigger(target, key)
  }
})

function track(target, key) {
  let depsMap = bucket.get(target)
  if (!depsMap) {
    bucket.set(target, (depsMap = new Map()))
  }
  let deps = depsMap.get(key)
  if (!deps) {
    depsMap.set(key, (deps = new Set()))
  }
  deps.add(activeEffect)
}

function trigger(target, key) {
  const depsMap = bucket.get(target)
  if (!depsMap) return
  const effects = depsMap.get(key)
  effects && effects.forEach(fn => fn())
}

// 用一个全局变量存储当前激活的 effect 函数
let activeEffect
function effect(fn) {
  activeEffect = fn
  fn()
}

effect(() => {
  console.log('effect run')
  document.body.innerText = obj.text
})

setTimeout(() => {
  trigger(data, 'text')
}, 1000)

</script>
```

##### 分支切换与cleanup

```javascript
effect(function effectfn(){
	document.body.innerText =obj.ok ? obj.text : 'not'
})
```

分支切换就是当obj.ok值发生变化时，代码执行的分支分支会跟着变化。上述代码的操作函数与响应数据之间的关联如下所示：

```
data
	--ok
	 	--okfn
	--text
		--textfn
```

当我们把obj.ok的值改为false，由于obj.text不会被读取，应该不会搜集操作函数textfn，然而目前的代码还是按照上述的依赖关系那样。此时就产生了遗留的操作函数。

我们可以来验证一下上述观点，在操作函数里打印下依赖关系：

首先将obj.ok设置为true

```javascript
// 原始数据
const data = { text: 'hello world',ok:true }

effect(() => {
  console.log('effect run')
  console.log(bucket.get(data))
  document.body.innerText = obj.ok ? obj.text : 'not'
})

setTimeout(() => {
  obj.text = 'hello vue3'
}, 1000)
//
0: {"ok" => Set(1)}
1: {"text" => Set(1)}
```

在定时器里将obj.ok设置为false

```javascript
// 原始数据
const data = { text: 'hello world'}

effect(() => {
  console.log('effect run')
  console.log(bucket.get(data))
  document.body.innerText = obj.ok ? obj.text : 'not'
})

setTimeout(() => {
  obj.ok = false
}, 1000)
//
0: {"ok" => Set(1)}
1: {"text" => Set(1)}
```

这里一下子搜集了两个依赖的原因也很简单，proxy在代理过程中访问了data对象，被get捕获器捕捉到了，就搜集了两个依赖。然而根据代码逻辑，obj.ok为false，页面值不会更改，不管如果修改obj.text,相关操作函数都不应该执行。我们需要在每次操作函数执行前，将其从所有的依赖中删除，

```html
<body></body>
<script>


// 存储副作用函数的桶
const bucket = new WeakMap()

// 原始数据
const data = { ok: true, text: 'hello world' }
// 对原始数据的代理
const obj = new Proxy(data, {
  // 拦截读取操作
  get(target, key) {
    // 将副作用函数 activeEffect 添加到存储副作用函数的桶中
    track(target, key)
    // 返回属性值
    return target[key]
  },
  // 拦截设置操作
  set(target, key, newVal) {
    // 设置属性值
    target[key] = newVal
    // 把副作用函数从桶里取出并执行
    trigger(target, key)
  }
})

function track(target, key) {
  let depsMap = bucket.get(target)
  if (!depsMap) {
    bucket.set(target, (depsMap = new Map()))
  }
  let deps = depsMap.get(key)
  if (!deps) {
    depsMap.set(key, (deps = new Set()))
  }
  deps.add(activeEffect)
  activeEffect.deps.push(deps)
}

function trigger(target, key) {
  const depsMap = bucket.get(target)
  if (!depsMap) return
  const effects = depsMap.get(key)

  const effectsToRun = new Set()
  effects && effects.forEach(effectFn => effectsToRun.add(effectFn))
  effectsToRun.forEach(effectFn => effectFn())
  // effects && effects.forEach(effectFn => effectFn())
}

// 用一个全局变量存储当前激活的 effect 函数
let activeEffect
function effect(fn) {
  const effectFn = () => {
    cleanup(effectFn)
    // 当调用 effect 注册副作用函数时，将副作用函数复制给 activeEffect
    activeEffect = effectFn
    fn()
  }
  // activeEffect.deps 用来存储所有与该副作用函数相关的依赖集合
  effectFn.deps = []
  // 执行副作用函数
  effectFn()
}

function cleanup(effectFn) {
  for (let i = 0; i < effectFn.deps.length; i++) {
    const deps = effectFn.deps[i]
    deps.delete(effectFn)
  }
  effectFn.deps.length = 0
}

effect(() => {
  console.log('effect run')
  console.log(bucket.get(data))
  document.body.innerText = obj.ok ? obj.text : 'not'
})

setTimeout(() => {
  obj.ok = false
  setTimeout(() => {
    obj.text = 'hello vue3'
  }, 1000)
}, 1000)

</script>
```

不太懂，明早继续看看





##### 嵌套的effect与effect栈





##### 避免无限递归

更改一下之前的effect代码

```javascript
const data = { ok: true, text: 'hello world',foo:0 }
...
effect(() => {
	obj.foo ++
})
```

运行下会发现控制台报栈溢出的错误，因为obj.foo ++有一个赋值操作，这就会引起trigger函数来调用对应的操作函数，而操作函数就是effect中的匿名函数，这就是一个递归调用，解决方案也比较简单，就是在调用操作函数之前判断下：trigger触发的函数和正在执行的函数是否一致即可：

```javascript
effects && effects.forEach(effectFn => {
    if (effectFn !== activeEffect) {
        effectsToRun.add(effectFn)
    }
})
```

##### 调度执行





##### 计算属性与lazy





##### watch实现原理





