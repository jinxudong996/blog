

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

前面只是对数据的处理，接下来才是对选项的合并。

在的最后有这样几行代码

```javascript
const options: ComponentOptions = {} as any
  let key
  for (key in parent) {
    mergeField(key)
  }
  for (key in child) {
    if (!hasOwn(parent, key)) {
      mergeField(key)
    }
  }
  function mergeField(key: any) {
    const strat = strats[key] || defaultStrat
    options[key] = strat(parent[key], child[key], vm, key)
  }
  return options
```

这里首先有两个for循环，意思就是将parent和child里面的key都调用mergeField方法，hasOwn方法是判断属性是否自己定义的而非原型上的，这样来防止重复合并。在mergeField函数中，定义了变量strat，它的值通过strats获取的，而strats是这样定义的：` const strats = config.optionMergeStrategies `，config是一个全局的配置对象，config.optionMergeStrategies是一个合并选项的策略对象，这个对象下包含很多函数，这些函数就可以认为是合并特定选项的策略。这样不同的选项使用不同的合并策略，如果你使用自定义选项，那么你也可以自定义该选项的合并策略，只需要在 `Vue.config.optionMergeStrategies` 对象上添加与自定义选项同名的函数就行。 

接下来看下有哪些合并策略。

##### el和propsData的合并策略

在[位置](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L27)定义了strats变量，随后就开始处理el和propsData

```javascript
if (__DEV__) {
  strats.el = strats.propsData = function (
    parent: any,
    child: any,
    vm: any,
    key: any
  ) {
    if (!vm) {
      warn(
        `option "${key}" can only be used during instance ` +
          'creation with the `new` keyword.'
      )
    }
    return defaultStrat(parent, child)
  }
}
```

这里首先判断是否是测试环境，然后定义了一个函数，先判断是否有vm，这里的vm就是通过mergeField函数传递的，也就是 mergeOptions函数的第三个参数，即vue实例。在策略函数中通过判断是否存在 `vm` 就能够得知 `mergeOptions` 是在实例化时调用(使用 `new` 操作符走 `_init` 方法)还是在继承时调用(`Vue.extend`)，而子组件的实现方式就是通过实例化子类完成的，子类又是通过 `Vue.extend` 创造出来的，所以我们就能通过对 `vm` 的判断而得知是否是子组件了。 

在函数中返回了defaultStrat函数，这个函数实际上也很简单

```js
const defaultStrat = function (parentVal: any, childVal: any): any {
  return childVal === undefined
    ? parentVal
    : childVal
}
```

defaultStrat 函数就如同它的名字一样，它是一个默认的策略，当一个选项不需要特殊处理的时候就使用默认的合并策略，它的逻辑很简单：只要子选项不是 `undefined` 那么就是用子选项，否则使用父选项。 

##### data的合并策略

在[这里](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L127)定义了data的合并函数

```js
strats.data = function (
  parentVal: any,
  childVal: any,
  vm?: Component
): Function | null {
  if (!vm) {
    if (childVal && typeof childVal !== 'function') {
      __DEV__ &&
        warn(
          'The "data" option should be a function ' +
            'that returns a per-instance value in component ' +
            'definitions.',
          vm
        )

      return parentVal
    }
    return mergeDataOrFn(parentVal, childVal)
  }

  return mergeDataOrFn(parentVal, childVal, vm)
}
```

这里主要是根据判断是否有vm来执行mergeDataOrFn函数，如果有vm，表明这里处理的是通过new实例化的组件，在mergeDataOrFn函数中多传递了个vm参数。

mergeDataOrFn在[这里](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L85)定义的，这里也是有一个是否vm的判断，上面就是根据是否是处理子组件来传递vm，同样这里也是根据是否传递了vm来判断是否是子组件。当没有vm即处理子组件时， 有两个if判断：如果没有子选项则使用父选项，没有父选项就直接使用子选项，且这两个选项都能保证是函数； 当父子选项同时存在，那么就返回一个函数 mergedDataFn；当有vm，即通过new操作符实例化的组件时，会直接返回 mergedInstanceDataFn 函数。 

也就是说data选项最终被 mergeOptions函数处理成了一个函数 ，都会调用函数 mergeData函数，代码在[这里](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L52)。

```javascript
function mergeData(
  to: Record<string | symbol, any>,
  from: Record<string | symbol, any> | null
): Record<PropertyKey, any> {
  if (!from) return to
  let key, toVal, fromVal

  const keys = hasSymbol
    ? (Reflect.ownKeys(from) as string[])
    : Object.keys(from)

  for (let i = 0; i < keys.length; i++) {
    key = keys[i]
    // in case the object is already observed...
    if (key === '__ob__') continue
    toVal = to[key]
    fromVal = from[key]
    if (!hasOwn(to, key)) {
      set(to, key, fromVal)
    } else if (
      toVal !== fromVal &&
      isPlainObject(toVal) &&
      isPlainObject(fromVal)
    ) {
      mergeData(toVal, fromVal)
    }
  }
  return to
}
```

`mergeData` 函数接收两个参数 `to` 和 `from`，根据 `mergeData` 函数被调用时参数的传递顺序我们知道，`to` 对应的是 `childVal` 产生的纯对象，`from` 对应 `parentVal` 产生的纯对象 。其作用也就是*将 `from` 对象的属性混合到 `to` 对象中，也可以说是将 `parentVal` 对象的属性混合到 `childVal` 中*，最后返回的是处理后的 `childVal` 对象。 

##### 生命周期钩子选择合并策略

[mergeLifecycleHook](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L153) 这个函数就是用来 合并生命周期钩子的。

```javascript
export function mergeLifecycleHook(
  parentVal: Array<Function> | null,
  childVal: Function | Array<Function> | null
): Array<Function> | null {
  const res = childVal
    ? parentVal
      ? parentVal.concat(childVal)
      : isArray(childVal)
      ? childVal
      : [childVal]
    : parentVal
  return res ? dedupeHooks(res) : res
}

function dedupeHooks(hooks: any) {
  const res: Array<any> = []
  for (let i = 0; i < hooks.length; i++) {
    if (res.indexOf(hooks[i]) === -1) {
      res.push(hooks[i])
    }
  }
  return res
}

LIFECYCLE_HOOKS.forEach(hook => {
  strats[hook] = mergeLifecycleHook
})
```

上面代码最后遍历了一个 `LIFECYCLE_HOOKS`  常量，这个[常量](https://github.com/vuejs/vue/blob/60d268c426/src/shared/constants.ts)就是生命周期钩子函数组成的一个数组， 它的作用就是在 `strats` 策略对象上添加用来合并各个生命周期钩子选项的策略函数，并且这些生命周期钩子选项的策略函数相同：都是 `mergeLifecycleHook` 函数。 

 而在`mergeLifecycleHook`函数中，也比较繁琐，是一个个三元表达式组成的，对其进行下翻译：

```js
return (是否有 childVal，即判断组件的选项中是否有对应名字的生命周期钩子函数)
  ? 如果有 childVal 则判断是否有 parentVal
    ? 如果有 parentVal 则使用 concat 方法将二者合并为一个数组
    : 如果没有 parentVal 则判断 childVal 是不是一个数组
      ? 如果 childVal 是一个数组则直接返回
      : 否则将其作为数组的元素，然后返回数组
  : 如果没有 childVal 则直接返回 parentVal
```

接下来举几个例子：

```js
new Vue({
  created: function () {
    console.log('created')
  }
})
```

比如这样的代码会被我们转化成

```js
options.created = [
  function () {
    console.log('created')
  }  
]
```

##### 资源assets选项的合并策略

 在 `Vue` 中 `directives`、`filters` 以及 `components` 被认为是资源。处理这些资源的函数 [mergeAssets ](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L188)，

```javascript
function mergeAssets(
  parentVal: Object | null,
  childVal: Object | null,
  vm: Component | null,
  key: string
): Object {
  const res = Object.create(parentVal || null)
  if (childVal) {
    __DEV__ && assertObjectType(key, childVal, vm)
    return extend(res, childVal)
  } else {
    return res
  }
}

ASSET_TYPES.forEach(function (type) {
  strats[type + 's'] = mergeAssets
})
```

 与生命周期钩子的合并处理策略基本一致 ，这个ASSET_TYPES变量里面就定义了`directives`、`filters` 以及 `components`这三个常量，只不过这个遍历再常量后面都加了个s。而在 mergeAssets函数中首先以 `parentVal` 为原型创建对象 `res`，然后判断是否有 `childVal`，如果有的话使用 `extend` 函数将 `childVal` 上的属性混合到 `res` 对象上并返回。如果没有 `childVal` 则直接返回 `res`。 

其中这行代码`const res = Object.create(parentVal || null)`通过Object.create来创建res，实际上算是res继承了parentVal的原型，包裹vue上的一些内置组件，比如keepalive，这也就是我们所有的vue组件都能够使用vue的内置组件一样。

##### watch的合并策略

合并[watch](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/util/options.ts#L213)函数的代码是在这里：

```javascript
strats.watch = function (
  parentVal: Record<string, any> | null,
  childVal: Record<string, any> | null,
  vm: Component | null,
  key: string
): Object | null {
  // work around Firefox's Object.prototype.watch...
  //@ts-expect-error work around
  if (parentVal === nativeWatch) parentVal = undefined
  //@ts-expect-error work around
  if (childVal === nativeWatch) childVal = undefined
  /* istanbul ignore if */
  if (!childVal) return Object.create(parentVal || null)
  if (__DEV__) {
    assertObjectType(key, childVal, vm)
  }
  if (!parentVal) return childVal
  const ret: Record<string, any> = {}
  extend(ret, parentVal)
  for (const key in childVal) {
    let parent = ret[key]
    const child = childVal[key]
    if (parent && !isArray(parent)) {
      parent = [parent]
    }
    ret[key] = parent ? parent.concat(child) : isArray(child) ? child : [child]
  }
  return ret
}
```

首先定义了 `ret` 常量，最后返回的也是 `ret` 常量，所以中间的代码是在充实 `ret` 常量。之后使用 `extend` 函数将 `parentVal` 的属性混合到 `ret` 中。然后开始一个 `for in` 循环遍历 `childVal`，这个循环的目的是：检测子选项中的值是否也在父选项中，如果在的话将父子选项合并到一个数组，否则直接把子选项变成一个数组返回。 



#### vue初始化

在vue的构造函数中，调用了[_init](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/init.ts#L17)方法

```javascript
if (options && options._isComponent) {
      // optimize internal component instantiation
      // since dynamic options merging is pretty slow, and none of the
      // internal component options needs special treatment.
      initInternalComponent(vm, options as any)
    } else {
      vm.$options = mergeOptions(
        resolveConstructorOptions(vm.constructor as any),
        options || {},
        vm
      )
    }
    /* istanbul ignore else */
    if (__DEV__) {
      initProxy(vm)
    } else {
      vm._renderProxy = vm
    }
```

其中mergeOptions函数就是前面的vue选项合并，并且将合并后的内容存储到vm.$options上，随后的if判断，如果是测试环境的话，就调用initProxy函数。这个[函数](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/proxy.ts#L84)的作用就是就是在实例对象 `vm` 上添加 `_renderProxy` 属性。 接下来仔细解读下：

```js
initProxy = function initProxy (vm) {
    if (hasProxy) {
        // determine which proxy handler to use
        const options = vm.$options
        const handlers = options.render && options.render._withStripped
        ? getHandler
        : hasHandler
        vm._renderProxy = new Proxy(vm, handlers)
    } else {
        vm._renderProxy = vm
    }
}
```

该函数接受一个vm实例作为参数，函数内有一个if判断，最终都会给vm添加一个_renderProx属性。其中如果宿主环境支持proxy的话，就执行这行代码:vm._renderProxy = new Proxy(vm, handlers).如果 `Proxy` 存在，那么将会使用 `Proxy` 对 `vm` 做一层代理，代理对象赋值给 `vm._renderProxy`，所以今后对 `vm._renderProxy` 的访问，如果有代理那么就会被拦截。代理对象配置参数是 `handlers`， 其中代理函数如下：

```js
const hasHandler = {
    has(target, key) {
      const has = key in target
      const isAllowed =
        allowedGlobals(key) ||
        (typeof key === 'string' &&
          key.charAt(0) === '_' &&
          !(key in target.$data))
      if (!has && !isAllowed) {
        if (key in target.$data) warnReservedPrefix(target, key)
        else warnNonPresent(target, key)
      }
      return has || !isAllowed
    }
  }
```

这里的代码意思就是在开发阶段给我们一些提示警告。其中  `allowedGlobals` 函数的作用是判断给定的 `key` 是否出现在上面字符串中定义的关键字中的。 warnReservedPrefix 通过 `warn` 打印一段警告信息，警告信息提示你“在渲染的时候引用了 `key`，但是在实例对象上并没有定义 `key` 这个属性或方法 。

至于会调用这个函数的原因就是：在render函数中有这样一行代码

```js
vnode = render.call(vm._renderProxy, vm.$createElement)
```

在调用render时将this指定为了vm._renderProxy。



######  初始化之 initLifecycle

在执行完 initProxy(vm) 后，执行了 initLifecycle(vm) 这行代码，这个[函数](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/lifecycle.ts#L34)就是初始化生命周期函数的，

```js
export function initLifecycle(vm: Component) {
  const options = vm.$options

  // locate first non-abstract parent
  let parent = options.parent
  if (parent && !options.abstract) {
    while (parent.$options.abstract && parent.$parent) {
      parent = parent.$parent
    }
    parent.$children.push(vm)
  }

  vm.$parent = parent
  vm.$root = parent ? parent.$root : vm

  vm.$children = []
  vm.$refs = {}

  vm._provided = parent ? parent._provided : Object.create(null)
  vm._watcher = null
  vm._inactive = null
  vm._directInactive = false
  vm._isMounted = false
  vm._isDestroyed = false
  vm._isBeingDestroyed = false
}
```

代码首先定义了 `vm.$options` 的引用 ，在定义了一个当前组件的父组件的实例，随后定义了一个whil循环，找到第一个非抽象组件的父组件， 并且在找到父级之后将当前实例添加到父实例的 `$children` 属性中。最后又向vm上添加了一些属性，比如常见的$children和$refs。

###### initEvents和 initRender 

初始化 `initLifecycle`  之后，代码执行了 [initEvents](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/events.ts#L12)

```js
export function initEvents(vm: Component) {
  vm._events = Object.create(null)
  vm._hasHookEvent = false
  // init parent attached events
  const listeners = vm.$options._parentListeners
  if (listeners) {
    updateComponentListeners(vm, listeners)
  }
}
```

 首先在 `vm` 实例对象上添加两个实例属性 `_events` 和 `_hasHookEvent`，其中 `_events` 被初始化为一个空对象，`_hasHookEvent` 的初始值为 `false` ，然后调用了`updateComponentListeners`函数。

然后开始执行`initRender`函数，

```js
export function initRender (vm: Component) {
  vm._vnode = null // the root of the child tree
  vm._staticTrees = null // v-once cached trees
  const options = vm.$options
  const parentVnode = vm.$vnode = options._parentVnode // the placeholder node in parent tree
  const renderContext = parentVnode && parentVnode.context
  vm.$slots = resolveSlots(options._renderChildren, renderContext)
  vm.$scopedSlots = emptyObject
  // bind the createElement fn to this instance
  // so that we get proper render context inside it.
  // args order: tag, data, children, normalizationType, alwaysNormalize
  // internal version is used by render functions compiled from templates
  vm._c = (a, b, c, d) => createElement(vm, a, b, c, d, false)
  // normalization is always applied for the public version, used in
  // user-written render functions.
  vm.$createElement = (a, b, c, d) => createElement(vm, a, b, c, d, true)

  // $attrs & $listeners are exposed for easier HOC creation.
  // they need to be reactive so that HOCs using them are always updated
  const parentData = parentVnode && parentVnode.data

  /* istanbul ignore else */
  if (process.env.NODE_ENV !== 'production') {
    defineReactive(vm, '$attrs', parentData && parentData.attrs || emptyObject, () => {
      !isUpdatingChildComponent && warn(`$attrs is readonly.`, vm)
    }, true)
    defineReactive(vm, '$listeners', options._parentListeners || emptyObject, () => {
      !isUpdatingChildComponent && warn(`$listeners is readonly.`, vm)
    }, true)
  } else {
    defineReactive(vm, '$attrs', parentData && parentData.attrs || emptyObject, null, true)
    defineReactive(vm, '$listeners', options._parentListeners || emptyObject, null, true)
  }
}
```

这里也是向vm上挂载一些属性和方法

随后在代码的末尾执行了生命周期函数：

```js
callHook(vm, 'beforeCreate', undefined, false /* setContext */)
initInjections(vm) // resolve injections before data/props
initState(vm)
initProvide(vm) // resolve provide after data/props
callHook(vm, 'created')
```

就是常见的beforeCreate和created这两个钩子函数。callHook就是执行具体的钩子函数，这个函数也比较简单，就是通过const handlers = vm.$options[hook]拿到对应的数组，遍历数组执行响应的函数。

此时，对生命周期钩子函数应该有了更深刻的理解： 其中 `initState` 包括了：`initProps`、`initMethods`、`initData`、`initComputed` 以及 `initWatch`。所以当 `beforeCreate` 钩子被调用时，所有与 `props`、`methods`、`data`、`computed` 以及 `watch` 相关的内容都不能使用，当然了 `inject/provide` 也是不可用的。 作为对立面，`created` 生命周期钩子则恰恰是等待 `initInjections`、`initState` 以及 `initProvide` 执行完毕之后才被调用，所以在 `created` 钩子中，是完全能够使用以上提到的内容的。但由于此时还没有任何挂载的操作，所以在 `created` 中是不能访问DOM的，即不能访问 `$el`。  



#### 响应式系统

在前面代码的最后执行了 `initData`  函数，这个[函数](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/state.ts#L122)是很多数据初始化函数的汇总，

```javascript
function initData(vm: Component) {
  let data: any = vm.$options.data
  data = vm._data = isFunction(data) ? getData(data, vm) : data || {}
  if (!isPlainObject(data)) {
    data = {}
    __DEV__ &&
      warn(
        'data functions should return an object:\n' +
          'https://v2.vuejs.org/v2/guide/components.html#data-Must-Be-a-Function',
        vm
      )
  }
  // proxy data on instance
  const keys = Object.keys(data)
  const props = vm.$options.props
  const methods = vm.$options.methods
  let i = keys.length
  while (i--) {
    const key = keys[i]
    if (__DEV__) {
      if (methods && hasOwn(methods, key)) {
        warn(`Method "${key}" has already been defined as a data property.`, vm)
      }
    }
    if (props && hasOwn(props, key)) {
      __DEV__ &&
        warn(
          `The data property "${key}" is already declared as a prop. ` +
            `Use prop default value instead.`,
          vm
        )
    } else if (!isReserved(key)) {
      proxy(vm, `_data`, key)
    }
  }
  // observe data
  const ob = observe(data)
  ob && ob.vmCount++
}
```

这个首先拿到前面合并选项后得到的data，前面知道data其实是一个函数，于是下面调用getData来拿到真正的data数据，

 `getData` 函数接收两个参数：第一个参数是 `data` 选项，我们知道 `data` 选项是一个函数，第二个参数是 `Vue` 实例对象。`getData` 函数的作用其实就是通过调用 `data` 函数获取真正的数据对象并返回，即：`data.call(vm, vm)`，而且我们注意到 `data.call(vm, vm)` 被包裹在 `try...catch` 语句块中，这是为了捕获 `data` 函数中可能出现的错误。同时如果有错误发生那么则返回一个空对象作为数据对象：`return {}`。 

随后代码做了一些判断与校验，比如data是否是一个纯对象，data、props、methods中的字段是否重复了；随后就开始对data进行代理`proxy(vm, `_data`, key)`，这样 当我们访问 `ins.a` 时实际访问的是 `ins._data.a`。而 `ins._data` 才是真正的数据对象。

最后代码执行了`const ob = observe(data)`，这个才是响应式的核心，

###### obserer

 将数据对象转换成响应式数据的是 `Observer` 函数，它是一个构造函数 ，代码位置：https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/observer/index.ts#L49。

首先看下他的构造函数：

```js
constructor(public value: any, public shallow = false, public mock = false) {
    // this.value = value
    this.dep = mock ? mockDep : new Dep()
    this.vmCount = 0
    def(value, '__ob__', this)
    if (isArray(value)) {
      if (!mock) {
        if (hasProto) {
          /* eslint-disable no-proto */
          ;(value as any).__proto__ = arrayMethods
          /* eslint-enable no-proto */
        } else {
          for (let i = 0, l = arrayKeys.length; i < l; i++) {
            const key = arrayKeys[i]
            def(value, key, arrayMethods[key])
          }
        }
      }
      if (!shallow) {
        this.observeArray(value)
      }
    } else {
      /**
       * Walk through all properties and convert them into
       * getter/setters. This method should only be called when
       * value type is Object.
       */
      const keys = Object.keys(value)
      for (let i = 0; i < keys.length; i++) {
        const key = keys[i]
        defineReactive(value, key, NO_INIITIAL_VALUE, undefined, shallow, mock)
      }
    }
  }
```

首先初始化了两个对象：dep为搜集依赖的一个实例；vmCount属性被设置为0。 初始化完成两个实例属性之后，使用 `def` 函数，为数据对象定义了一个 `__ob__` 属性，这个属性的值就是当前 `Observer` 实例对象。其中 `def` 函数其实就是 `Object.defineProperty` 函数的简单封装，之所以这里使用 `def` 函数定义 `__ob__` 属性是因为这样可以定义不可枚举的属性，这样后面遍历数据对象的时候就能够防止遍历到 `__ob__` 属性。 

假如有这样一个数据：

```js
const data = {
  a: 1
}
```

那么经过 `def` 函数处理之后，`data` 对象应该变成如下这个样子：

```js
const data = {
  a: 1,
  // __ob__ 是不可枚举的属性
  __ob__: {
    value: data, // value 属性指向 data 数据对象本身，这是一个循环引用
    dep: dep实例对象, // new Dep()
    vmCount: 0
  }
}
```

随后代码区分数据是数组还是纯对象，如果是对象的话，遍历对象，为每个对象的属性调用 `defineReactive`  函数， `defineReactive` 函数的核心就是 将数据对象的数据属性转换为访问器属性，即为数据对象的属性设置一对 `getter/setter`，但其中做了很多处理边界条件的工作。 代码位置：https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/observer/index.ts#L131。在`defineReactive` 函数中，都会为每个属性定义一个新的dep实例，每个属性都有自己的dep对象。然后使用 `Object.defineProperty` 函数将每个属性都转化为访问器属性，同时在get函数中调用 dep.depend() 搜集依赖；随后在set中触发依赖，首先调用const value = getter ? getter.call(obj) : val拿到上一次改动的值，与当前的值做一个对比，如果不一样再调用dep.notify()触发依赖。







这个函数定义在[这里](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/observer/index.ts#L105)，



#### 渲染函数的观察者与进阶的数据响应式系统

###### $mount挂载函数

在构造函数所有的初始化完成后就开始调用vue.$mount方法。他首先缓存了运行时版本的mount方法，接下来重写了该方法，实际上就是为运行时版添加模板编译的功能。

首先mount方法判断挂载点是不是body和html，挂载实际上就是替换，而这两个是不能被替换的。

 实际上完整版 `Vue` 的 `$mount` 函数要做的核心事情就是编译模板(`template`)字符串为渲染函数，并将渲染函数赋值给 `vm.$options.render` 选项，这个选项将会在真正挂载组件的 `mountComponent` 函数中。 



###### 渲染函数的观察者

真正挂载的方法就是mountComponent 。这里定义并初始化 `updateComponent` 函数，这个函数将用作创建 `Watcher` 实例时传递给 `Watcher` 构造函数的第二个参数， 

 正是因为 `watcher` 对表达式的求值，触发了数据属性的 `get` 拦截器函数，从而收集到了依赖，当数据变化时能够触发响应。在上面的代码中 `Watcher` 观察者实例将对 `updateComponent` 函数求值，我们知道 `updateComponent` 函数的执行会间接触发渲染函数(`vm.$options.render`)的执行，而渲染函数的执行则会触发数据属性的 `get` 拦截器函数，从而将依赖(`观察者`)收集，当数据变化时将重新执行 `updateComponent` 函数，这就完成了重新渲染。同时我们把上面代码中实例化的观察者对象称为 **渲染函数的观察者**。 

 `updateComponent` 函数的作用就是：**把渲染函数生成的虚拟DOM渲染成真正的DOM** 

 `Watcher` 类的 `constructor` 方法可以知道在创建 `Watcher` 实例时可以传递五个参数，分别是：组件实例对象 `vm`、要观察的表达式 `expOrFn`、当被观察的表达式的值变化时的回调函数 `cb`、一些传递给当前观察者对象的选项 `options` 以及一个布尔值 `isRenderWatcher` 用来标识该观察者实例是否是渲染函数的观察者。 

 `Watcher` 的原理是通过对“被观测目标”的求值，触发数据属性的 `get` 拦截器函数从而收集依赖，至于“被观测目标”到底是表达式还是函数或者是其他形式的内容都不重要，重要的是“被观测目标”能否触发数据属性的 `get` 拦截器函数，很显然函数是具备这个能力的。 

 该组件实例的观察者都会被添加到该组件实例对象的 `vm._watchers` 数组中 



 无论是 `Vue` 的 `watch` 选项还是 `vm.$watch` 函数，他们的实现都是通过实例化 `Watcher` 类完成的， 



 每个响应式数据的属性都通过闭包引用着一个用来收集属于自身依赖的“筐”，实际上那个“筐”就是 `Dep` 类的实例对象。 



避免重复搜集依赖：

 在 `addDep` 内部并不是直接调用 `dep.addSub` 收集观察者，而是先根据 `dep.id` 属性检测该 `Dep` 实例对象是否已经存在于 `newDepIds` 中，如果存在那么说明已经收集过依赖了，什么都不会做。如果不存在才会继续执行 `if` 语句块的代码，同时将 `dep.id` 属性和 `Dep` 实例对象本身分别添加到 `newDepIds` 和 `newDeps` 属性中，这样无论一个数据属性被读取了多少次，对于同一个观察者它只会收集一次。 



###### 异步渲染

每次修改属性的值之后并没有立即重新求值，而是将需要执行更新操作的观察者放入一个队列中。当我们修改 `name` 属性值时，由于 `name` 属性收集了渲染函数的观察者(后面我们称其为 `renderWatcher`)作为依赖，所以此时 `renderWatcher` 会被添加到队列中，接着我们修改了 `age` 属性的值，由于 `age` 属性也收集了 `renderWatcher` 作为依赖，所以此时也会尝试将 `renderWatcher` 添加到队列中，但是由于 `renderWatcher` 已经存在于队列中了，所以并不会重复添加，这样队列中将只会存在一个 `renderWatcher`。当所有的突变完成之后，再一次性的执行队列中所有观察者的更新方法，同时清空队列，这样就达到了优化的目的。 



 `$watch` 方法的实现本质就是创建了一个 `Watcher` 实例对象。 



###### watch原理

 我们知道当一个属性与一个观察者建立联系之后，属性的 `Dep` 实例对象会收集到该观察者对象，同时观察者对象也会将该 `Dep` 实例对象收集，这是一个双向的过程，并且一个观察者可以同时观察多个属性，这些属性的 `Dep` 实例对象都会被收集到该观察者实例对象的 `this.deps` 数组中，所以解除属性与观察者之间关系的第二步就是将当前观察者实例对象从所有的 `Dep` 实例对象中移除， 



#### 其他重要选项的初始化及实现





#### vue编译器



#### 生产AST



#### 



#### 