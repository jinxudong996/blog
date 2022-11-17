##### 源码解读

vue响应式的起源是从这个[函数](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/state.ts#L122)开始的，也就是我们的`initData`函数

```js
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

这个首先拿到data数据对象，一般在写data时都会写成一个data函数，就通过调用getData来拿到真正的data数据，随后有一个if判断，来检查开发环境的data是不是一个纯对象，这里判断是否是对象的方法也比较简单，是通过`Object.prototype.toString.call()`来判断的。也就是说我们的data，在开发时需要是一个函数，而且返回一个纯对象。

接下来就开始校验`method`、`props`和`data`中的属性是否重复。首先拿到所有data的key组成的数组，然后遍历该数组，通过`hasOwn`方法来判断是否有重复的，[hasOwn](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwn)方法可以判断对象自身的属性。

随后校验我们属性命名规范后，调用proxy方法来对data中的属性做一个代理。` proxy(vm, `_data`, key)`，这个[proxy](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/instance/state.ts#L42)方法也是通过` Object.defineProperty(target, key, sharedPropertyDefinition) `这行代码对data中的属性进行代理， 当我们访问 `ins.a` 时实际访问的是 `ins._data.a`。而 `ins._data` 才是真正的数据对象。 

在经过一系列的校验后就开始了响应式真正开始的地方，` const ob = observe(data) `。



###### observe工厂函数

[observe](https://github.com/vuejs/vue/blob/60d268c4261a0b9c5125f308468b31996a8145ad/src/core/observer/index.ts#L105)函数实际上是一个工厂函数，这里先介绍下工厂函数。

javascript高级程序设计中写了个工厂函数来创建对象，

```js
function createPerson(name, age, job) {
 	let o = new Object();
 	o.name = name;
 	o.age = age;
 	o.job = job;
 	o.sayName = function() {
 	console.log(this.name);
 };
 return o;
}
let person1 = createPerson("Nicholas", 29, "Software Engineer");
let person2 = createPerson("Greg", 27, "Doctor"); 
```

工厂方法模式是将创建实例推迟到子类中进行，也就是一种封装方法，有了工厂模式我们构建对象不需要关注对象构建的过程，我们需要的对象只需要想工厂发出生产对象的指令就可以了。抛弃构建的复杂过程，增加代码的阅读性。

回到observe函数，这个函数也比较简单：

```js
export function observe(
  value: any,
  shallow?: boolean,
  ssrMockReactivity?: boolean
): Observer | void {
  if (!isObject(value) || isRef(value) || value instanceof VNode) {
    return
  }
  let ob: Observer | void
  if (hasOwn(value, '__ob__') && value.__ob__ instanceof Observer) {
    ob = value.__ob__
  } else if (
    shouldObserve &&
    (ssrMockReactivity || !isServerRendering()) &&
    (isArray(value) || isPlainObject(value)) &&
    Object.isExtensible(value) &&
    !value.__v_skip /* ReactiveFlags.SKIP */
  ) {
    ob = new Observer(value, shallow, ssrMockReactivity)
  }
  return ob
}
```

这里先对我们传入的对象做校验，随后申明一个变量ob用来存储Observe实例。









##### 简单实现