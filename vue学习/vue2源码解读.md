

#### vue静态成员和实力成员初始化过程

##### 构造函数

```js
//./instance/index.js
// 从五个文件导入五个方法（不包括 warn）
import { initMixin } from './init'
import { stateMixin } from './state'
import { renderMixin } from './render'
import { eventsMixin } from './events'
import { lifecycleMixin } from './lifecycle'
import { warn } from '../util/index'

// 定义 Vue 构造函数
function Vue (options) {
  if (process.env.NODE_ENV !== 'production' &&
    !(this instanceof Vue)
  ) {
    warn('Vue is a constructor and should be called with the `new` keyword')
  }
  this._init(options)
}

// 将 Vue 作为参数传递给导入的五个方法
initMixin(Vue)
stateMixin(Vue)
eventsMixin(Vue)
lifecycleMixin(Vue)
renderMixin(Vue)

// 导出 Vue
export default Vue
```

接下来一一看下这五个方法

- initMixin

  定义在当前路径下的`init.js`

  ```js
  export function initMixin (Vue: Class<Component>) {
    Vue.prototype._init = function (options?: Object) {
      // ... _init 方法的函数体，此处省略
    }
  }
  ```

  可以看到这个方法就是在vue原型上添加了个_init方法，这应该是一个内部初始化的方法。而这个方法再vue 的构造函数中调用了`this._init(options)`

- stateMixin

  这个方法定义在`state.js`下，代码位置：https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/state.ts#L335

  这里在vue的原型上定义了五个方法，分别是：` $data `，$`props`，` $set `，`$delete`和` $watch `。其中 `$data` 属性实际上代理的是 `_data` 这个实例属性，而 `$props` 代理的是 `_props` 这个实例属性；而且还对`$set`做了下判断，测试还是不允许修改的。



​		

- eventsMixin

  代码位置：https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/events.ts#L59

  这里在vue原型上添加了四个方法

  ```js
  Vue.prototype.$on = function (event: string | Array<string>, fn: Function): Component {}
  Vue.prototype.$once = function (event: string, fn: Function): Component {}
  Vue.prototype.$off = function (event?: string | Array<string>, fn?: Function): Component {}
  Vue.prototype.$emit = function (event: string): Component {}
  ```

- lifecycleMixin

  代码地址：https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/lifecycle.ts#L61

  这里在原型上定义了三个方法：

  ```js
  Vue.prototype._update = function (vnode: VNode, hydrating?: boolean) {}
  Vue.prototype.$forceUpdate = function () {}
  Vue.prototype.$destroy = function () {}
  ```

  

- renderMixin

  代码位置：https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/render.ts#L95

  函数开始就调用了` installRenderHelpers(Vue.prototype) `， installRenderHelpers这个函数也是往原型上添加各种方法

  ```javascript
  export function installRenderHelpers (target: any) {
    target._o = markOnce
    target._n = toNumber
    target._s = toString
    target._l = renderList
    target._t = renderSlot
    target._q = looseEqual
    target._i = looseIndexOf
    target._m = renderStatic
    target._f = resolveFilter
    target._k = checkKeyCodes
    target._b = bindObjectProps
    target._v = createTextVNode
    target._e = createEmptyVNode
    target._u = resolveScopedSlots
    target._g = bindObjectListeners
  }
  ```

  同时还定义了` $nextTick `和`_render`方法。

##### vue选项规范化

根据前文我们知道vue的[构造函数](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/index.ts#L9)，在构造函数里执行了`this._init(options)`这行代码， 下面我们就看看 `_init` 做了什么 。代码位置：https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/init.ts#L17。

首先是这样两行代码

```js
const vm: Component = this
// a uid
vm._uid = uid++
```

最后打开mergeOptions定的[地方](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L395)，继续学习。

###### 检查组件名称

mergeOptions代码第一行就是一个判断语句：

```javascript
if (__DEV__) {
    checkComponents(child)
}
```

这里的[checkComponents](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L277)主要是检查我们的组价名称是否符合规范，

- ①：组件的名字要满足正则表达式：`/^[a-zA-Z][\w-]*$/`
- ②：要满足：条件 `isBuiltInTag(name) || config.isReservedTag(name)` 不成立

然后再通过`isBuiltInTag`和`isReservedTag`来检查组件名称是否是内置的标签，就类似于函数命名时不能使用关键字，比如vue中的 slot和component。 

接下来的代码是

```javascript
if (isFunction(child)) {
    // @ts-expect-error
    child = child.options
}
```

这说明 `child` 参数除了是普通的选项对象外，还可以是一个函数，如果是函数的话就取该函数的 `options` 静态属性作为新的 `child`，我们想一想什么样的函数具有 `options` 静态属性呢？现在我们知道 `Vue` 构造函数本身就拥有这个属性，其实通过 `Vue.extend` 创造出来的子类也是拥有这个属性的。所以这就允许我们在进行选项合并的时候，去合并一个 `Vue` 实例构造者的选项了。 

###### 规范化props

接下来就是三个规范化选项的函数调用

```js
normalizeProps(child, vm)
normalizeInject(child, vm)
normalizeDirectives(child)
```

在写vue代码时，props的写法是很灵活的，有两种方式：

数组：

```js
const ChildComponent = {
  props: ['someData']
}
```

对象：

```js
const ChildComponent = {
  props: {
    someData: {
      type: Number,
      default: 0
    }
  }
}
```

规范props的函数 normalizeProps 在这里[定义的](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L307)，

```javascript
if (isArray(props)) {
    i = props.length
    while (i--) {
      val = props[i]
      if (typeof val === 'string') {
        name = camelize(val)
        res[name] = { type: null }
      } else if (__DEV__) {
        warn('props must be strings when using array syntax.')
      }
    }
  } else if (isPlainObject(props)) {
    for (const key in props) {
      val = props[key]
      name = camelize(key)
      res[name] = isPlainObject(val) ? val : { type: val }
    }
  }
```

在代码中也分为了两种情况，首先是数组的话，通过`camelize(val)`将中横线转驼峰 。 然后在 `res` 对象上添加了与转驼峰后的 `props` 同名的属性，其值为 `{ type: null }` 。

如果props是对象类型的话，遍历对象

```js
val = props[key]
name = camelize(key)
res[name] = isPlainObject(val) ? val : { type: val }
```

先将变量名规范下，在判断变量值是对象的话就不变，不然那就是`{ type: val }`。

###### 规范化inject

 normalizeInject 是在这里[定义](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L342)的，这个函数是用来规范inject选项的。这里可以回顾下[文档](https://v2.cn.vuejs.org/v2/api/#provide-inject)，用来父子组件之间通信的。这里有一个简单的例子

```js
/ 子组件
const ChildComponent = {
  template: '<div>child component</div>',
  created: function () {
    // 这里的 data 是父组件注入进来的
    console.log(this.data)
  },
  inject: ['data'],
  //inject: {
  //  d: 'data'
  //}
}

// 父组件
var vm = new Vue({
  el: '#app',
  // 向子组件提供数据
  provide: {
    data: 'test provide'
  },
  components: {
    ChildComponent
  }
})
```

这里inject接受privede的数据和props一样，都是可以数组或者是对象的形式。如果是数组的形式，主要是这行代码`normalized[inject[i]] = { from: inject[i] }`，将`['data1', 'data2']`转化为

```js
{
  'data1': { from: 'data1' },
  'data2': { from: 'data2' }
}
```

如果是对象的话，

```js
normalized[key] = isPlainObject(val)
      ? extend({ from: key }, val)
      : { from: val }
```

将这样的代码

```js
inject: {
  data1,
  d2: 'data2',
  data3: { someProperty: 'someValue' }
}
```

转化为

```js
inject: {
  'data1': { from: 'data1' },
  'd2': { from: 'data2' },
  'data3': { from: 'data3', someProperty: 'someValue' }
}
```

###### 规范化directives

规范 directives的normalizeDirectives 函数在这个里[定义](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L369)的， directives用来注册局部指令的，也比较简单，核心代码就是`dirs[key] = { bind: def, update: def }`， 将该函数作为对象形式的 `bind` 属性和 `update` 属性的值。也就是说，可以把使用函数语法注册指令的方式理解为一种简写。



#### vue选项合并





#### vue初始化







#### 响应式系统







#### 渲染函数的观察者与进阶的数据响应式系统







#### 其他重要选项的初始化及实现





#### vue编译器



#### 生产AST



#### 



#### 