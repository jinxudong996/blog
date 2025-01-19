

#### 框架搭建

先仿照下vue3的代码组织结构，搭建下基本都框架

接下来开始以vue3源码为例，开始搭建我们的mini-vue3

1. 运行`npm init -y`创建 package.json 模块 
2. 创建 packages 文件夹，作为：核心代码 区域 
3. 创建 packages/vue 文件夹：打包、测试实例、项目整体入口模块 
4. 创建 packages/shared 文件夹：共享公共方法模块 
5. 创建 packages/compiler-core 文件夹：编辑器核心模块 
6. 创建 packages/compiler-dom 文件夹：浏览器部分编辑器模块 
7. 创建 packages/reactivity 文件夹：响应性模块 
8. 创建 packages/runtime-core 文件夹：运行时核心模块 
9. 创建 packages/runtime-dom 文件夹：浏览器部分运行时模块 

接下来导入TS

```js
// 需要先安装 typescript
npm install -g typescript@4.7.4
// 生成默认配置
tsc -init
```

新建文件`tsconfig.json`

```json
{
	// 编辑器配置
	"compilerOptions": {
		// 根目录
		"rootDir": ".",
		// 严格模式标志
		"strict": true,
		// 指定类型脚本如何从给定的模块说明符查找文件。
		"moduleResolution": "node",
		// https://www.typescriptlang.org/tsconfig#esModuleInterop
		"esModuleInterop": true,
		// JS 语言版本
		"target": "es5",
		// 允许未读取局部变量
		"noUnusedLocals": false,
		// 允许未读取的参数
		"noUnusedParameters": false,
		// 允许解析 json
		"resolveJsonModule": true,
		// 支持语法迭代：https://www.typescriptlang.org/tsconfig#downlevelIteration
		"downlevelIteration": true,
		// 允许使用隐式的 any 类型（这样有助于我们简化 ts 的复杂度，从而更加专注于逻辑本身）
		"noImplicitAny": false,
		// 模块化
		"module": "esnext",
		// 转换为 JavaScript 时从 TypeScript 文件中删除所有注释。
		"removeComments": false,
		// 禁用 sourceMap
		"sourceMap": false,
		// https://www.typescriptlang.org/tsconfig#lib
		"lib": ["esnext", "dom"],
		// 设置快捷导入
		"baseUrl": ".",
		"paths": {
      "@vue/*": ["packages/*/src"]
    }
	},
	// 入口
	"include": [
		"packages/*/src"
	]
}

```

导入 rollup ，选择` rollup `而非`webpack`对于开发库而言，` rollup `更加适合，不会产生冗余代码。

新建`rollup.config.js`

```js
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import typescript from "@rollup/plugin-typescript";

/**
 * 默认导出一个数组，数组的每一个对象都是一个单独的导出文件配置，详细可查：https://www.rollupjs.com/guide/big-list-of-options
 */
export default [
  {
    // 入口文件
    input: "packages/vue/src/index.ts",
    // 打包出口
    output: [
      // 导出 iife 模式的包
      {
        // 开启 SourceMap
        sourcemap: true,
        // 导出的文件地址
        file: "./packages/vue/dist/vue.js",
        // 生成的包格式：一个自动执行的功能，适合作为<script>标签
        format: "iife",
        // 变量名
        name: "Vue",
      },
    ],
    // 插件
    plugins: [
      // ts 支持
      typescript({ sourceMap: true }),
      // 模块导入的路径补全
      resolve(),
      // 将 CommonJS 模块转换为 ES2015
      commonjs(),
    ],
  },
];

```

添加打包命令`"dev": "rollup -c -w",` 运行`npm run dev`时，可以看到产生了`packages/vue/dist/vue.js`文件

#### 响应式

vue2的响应式都是以`Object.defineProperty`来实现的，但是这个API有很大的缺陷：

1. 当为对象新增一个没有在 data 中声明的属性时，新增的属性 不是响应性 的 

2. 当为数组通过下标的形式新增一个元素时，新增的元素不是响应性的

于是vue3使用了[Proxy](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Proxy)这个API来重构了响应式系统。看下下面的一个简答的小例子

```js
const target = {
  name: 'Alice',
  age: 25
};

// 定义一个处理器对象，包含拦截逻辑
const handler = {
  // 拦截属性访问
  get(target, prop, receiver) {
    console.log(`Getting property: ${String(prop)}`);
    return Reflect.get(target, prop, receiver);
  },
  // 拦截属性设置
  set(target, prop, value, receiver) {
    console.log(`Setting property: ${String(prop)} to ${value}`);
    return Reflect.set(target, prop, value, receiver);
  }
};

// 创建代理对象
const proxy = new Proxy(target, handler);

// 访问和设置代理对象的属性
console.log(proxy.name); // 输出: Getting property: name
                         // 输出: Alice

proxy.age = 26;          // 输出: Setting property: age to 26

console.log(proxy.age);  // 输出: Getting property: age
                         // 输出: 26
```

一般Proxy都会和[Reflect](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Reflect)搭配使用，实际上Proxy本身也有拦截器，为何还要使用Reflect，看下这个例子就知道了

```js
const p1 = {
  lastName: "张",
  firstName: "三",
  // 通过 get 标识符标记，可以让方法的调用像属性的调用一样
  get fullName() {
    return this.lastName + this.firstName;
  },
};
const proxy = new Proxy(p1, {
  // target：被代理对象
  // receiver：代理对象
  get(target, key, receiver) {
    console.log("触发了 getter");
    return target[key];
  },
});
console.log(proxy.fullName);

```

上面代码中get中的log只会打印一次，如果想让`this.lastName + this.firstName`也会触发代理中的get方法，怎么做呢，就需要用到`Reflect.get`

```js
const proxy = new Proxy(p1, {
  // target：被代理对象
  // receiver：代理对象
  get(target, key, receiver) {
    console.log("触发了 getter");
    // return target[key];
    return Reflect.get(target, key, receiver);
  },
});
```

修改后就能完美的触发三次getter了。

###### 源码阅读

首先去[github](https://github.com/vuejs/core)上拉取代码，安装依赖。在`package.json`中可以看到运行打包的命令`"build": "node scripts/build.js",`打开`build.js`有下面这样一段代码

```js
const { values, positionals: targets } = parseArgs({
  allowPositionals: true,
  options: {
    formats: {
      type: 'string',
      short: 'f',
    },
    devOnly: {
      type: 'boolean',
      short: 'd',
    },
    prodOnly: {
      type: 'boolean',
      short: 'p',
    },
    withTypes: {
      type: 'boolean',
      short: 't',
    },
    sourceMap: {
      type: 'boolean',
      short: 's',
    },
    release: {
      type: 'boolean',
    },
    all: {
      type: 'boolean',
      short: 'a',
    },
    size: {
      type: 'boolean',
    },
  },
})
```

就是用于解析命令行输入的参数，并将它们分类为命名选项和位置参数， 其中我们需要打开`sourceMap`，可以使用 `-s` 或 `--sourceMap` 指定。 然后更改下打包命令：

```json
"build": "node scripts/build.js -s",
```

然后新建测试用例`packages/vue/example/text/index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <script src="../../dist/vue.global.js"></script>
  </head>
  <body>
    <div id="app"></div>
  </body>
  <script>
    // 从 Vue 中结构出 reactie、effect 方法
    const { reactive, effect } = Vue
    // 声明响应式数据 obj
    const obj = reactive({
      name: '张三',
    })
    // 调用 effect 方法
    effect(() => {
      document.querySelector('#app').innerText = obj.name
    })
    // 定时修改数据，视图发生变化
    setTimeout(() => {
      obj.name = '李四'
    }, 2000)
  </script>
</html>

```

然后打开浏览器，在`reactive`调用处打上断点，就可以调试vue3的源码了

![1737012318646](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1737012318646.png)



vue3中想要拥有响应式数据有两种方式，reactive和ref，接下来仿照源码完成代码编写

###### reactive

首先看下reactive方法在源码中做了啥：

reactive方法定义在`reactivity/src/reactive.ts`中，返回了createReactiveObject方法，单步进入createReactiveObject方法，核心代码是这样

```js
const proxy = new Proxy(
    target,
    targetType === TargetType.COLLECTION ? collectionHandlers : baseHandlers,
 )
 proxyMap.set(target, proxy)
 return proxy
```

`new Proxy`创建了一个代理对象，其中Proxy第一个参数是我们的目标对象，在测试实例中就是`{name:张三}`，第二个参数就是baseHandlers，而这个baseHandlers是createReactiveObject的第三个参数shallowReadonlyHandlers，而这个shallowReadonlyHandlers定义在`baseHandlers.ts`中，代码实例化了ReadonlyReactiveHandler，ReadonlyReactiveHandler继承了BaseReactiveHandler，定义了一些静态方法：set和deleteProperty方法；



然后将代理对象放入到proxyMap里面，再将这个代理对象proxy返回。

接下来看下effect源码部分：

effect方法定义在`reactivity/src/effect.ts`中，有这样一段代码`const e = new ReactiveEffect(fn)`

其中fn就是我们的副作用函数，也就是传入effect方法的，而ReactiveEffect内部定义了notify、run、stop和trigger等方法，后面代码又执行了这个run方法。run方法中执行了我们传入的副作用函数。

而副作用函数会读取obj的属性，而obj经过reactive的处理已经变成了一个代理对象，这就会触发BaseReactiveHandler中定义的get方法，get方法中有这样一段代码

```js
//class BaseReactiveHandler implements ProxyHandler
const res = Reflect.get(
      target,
      key,
      // if this is a proxy wrapping a ref, return methods using the raw ref
      // as receiver so that we don't have to call `toRaw` on the ref in all
      // its class methods
      isRef(target) ? target : receiver,
    )
```

利用Reflect来读取代理对象的值，随后就执行了`track(target, TrackOpTypes.GET, key)`，这个track方法就是vue响应式中的搜集依赖。

track方法定义在`reactivity/src/dep.ts`中，核心代码如下

```js
let depsMap = targetMap.get(target)
if (!depsMap) {
    targetMap.set(target, (depsMap = new Map()))
}
let dep = depsMap.get(key)
if (!dep) {
    depsMap.set(key, (dep = new Dep()))
    dep.map = depsMap
    dep.key = key
}
if (__DEV__) {
    dep.track({
        target,
        type,
        key,
    })
} else {
    dep.track()
}
```

就是将我们的targetMap转化为这样的

```
1. key ： target
2. value ： Map
    1. key ： key
    2. value ： Set
```

随后又执行了`dep.track()`方法。这里最新的3.5.13代码没看懂如何搜集的副作用函数，猜测应该是`addSub(link)`这行代码，但是link的数据结构太复杂。相比3.2版本的就很容易了，track中执行了`trackEffects(dep, eventInfo)，`，trackEffects中有这样一句`dep.add(activeEffect!)`，这个activeEffect就是我们的副作用函数，最终的targetMap会变成

```
1. key ： target
2. value ： Map
    1. key ： key
    2. value ： [fn]
```

在测试用例中，2s后执行`obj.name = '李四'`，这个会触发set方法，这个方法定义在MutableReactiveHandler这个类里，和get方法类似，也使用了Reflect

```js
const result = Reflect.set(
      target,
      key,
      value,
      isRef(target) ? target : receiver,
    )
```

在最后还执行了这行代码

```js
trigger(target, TriggerOpTypes.SET, key, value, oldValue)
```

这就是vue响应式系统中的触发依赖。

trigger方法定义在`dep.ts`中，代码最终执行了`dep.trigger`

```js
dep.trigger({
    target,
    type,
    key,
    newValue,
    oldValue,
    oldTarget,
})
```

trigger中执行了`this.notify(debugInfo)`，

```js
for (let link = this.subs; link; link = link.prevSub) {
        if (link.sub.notify()) {
          // if notify() returns `true`, this is a computed. Also call notify
          // on its dep - it's called here instead of inside computed's notify
          // in order to reduce call stack depth.
          ;(link.sub as ComputedRefImpl).dep.notify()
        }
      }
```

这里还是3.2版本的更加清晰点，在triggerEffects中执行effect.run()，run方法中this.fn()，这个fn就是传入effect的副作用函数。

总结下，set方法中干了两件事，修改obj的值和targetMap 下保存的 fn 函数。接下来就开始仿写下相关代码。

###### 基本架构

新建文件`packages/vue/src/index.ts`当做我们的入口文件

```js
export { reactive } from '@vue/reactivity'
```

新建`packages/reactivitysrc/index.ts`

```js
export { reactive } from './reactive'
```

新建`packages/reactivitysrc/reactive.ts`

```js
import { mutableHandlers } from "./baseHandlers";
/**
 * 响应性 Map 缓存对象
 * key：target
 * val：proxy
 */
export const reactiveMap = new WeakMap<object, any>();
/**
 * 为复杂数据类型，创建响应性对象
 * @param target 被代理对象
 * @returns 代理对象
 */
export function reactive(target: object) {
  return createReactiveObject(target, mutableHandlers, reactiveMap);
}
/**
 * 创建响应性对象
 * @param target 被代理对象
 * @param baseHandlers handler
 */
function createReactiveObject(
  target: object,
  baseHandlers: ProxyHandler<any>,
  proxyMap: WeakMap<object, any>
) {
  // 如果该实例已经被代理，则直接读取即可
  const existingProxy = proxyMap.get(target);
  if (existingProxy) {
    return existingProxy;
  }
  // 未被代理则生成 proxy 实例
  const proxy = new Proxy(target, baseHandlers);
  // 缓存代理对象
  proxyMap.set(target, proxy);
  return proxy;
}

```

这里的核心代码就是createReactiveObject方法，方法接受三个三个参数，代理对象，处理方法以及map缓存对象，首先判断如果缓存对象里有目标对象，就直接返回，如果没有就通过proxy代理目标对象。

这里的baseHandlers在`baseHandlers.js`中定义的

```js
import { track, trigger } from "./effect";

/**
 * getter 回调方法
 */
const get = createGetter();
/**
 * 创建 getter 回调方法
 */
function createGetter() {
  return function get(target: object, key: string | symbol, receiver: object) {
    // 利用 Reflect 得到返回值
    const res = Reflect.get(target, key, receiver);
    // 收集依赖
    track(target, key);
    return res;
  };
}

/**
 * setter 回调方法
 */
const set = createSetter();
/**
 * 创建 setter 回调方法
 */
function createSetter() {
  return function set(
    target: object,
    key: PropertyKey,
    value: unknown,
    receiver: object
  ) {
    // 利用 Reflect.set 设置新值
    const result = Reflect.set(target, key, value, receiver);
    // 触发依赖
    trigger(target, key, value);
    return result;
  };
}

export const mutableHandlers: ProxyHandler<object> = {
  get,
  set,
};

```

其中get方法就是常规的读取目标对象中的值，在读取时还用track方法搜集依赖；set方法就是设置新值，设置新值的时候调用trigger触发依赖。

这里的track方法和trigger方法定义在`effect.ts`中

```js
/**
 * 用于收集依赖的方法
 * @param target WeakMap 的 key
 * @param key 代理对象的 key，当依赖被触发时，需要根据该 key 获取
 */
export function track(target: object, key: unknown) {
  console.log("track: 收集依赖");
}
/**
 * 触发依赖的方法
 * @param target WeakMap 的 key
 * @param key 代理对象的 key，当依赖被触发时，需要根据该 key 获取
 * @param newValue 指定 key 的最新值
 * @param oldValue 指定 key 的旧值
 */
export function trigger(target: object, key?: unknown, newValue?: unknown) {
  console.log("trigger: 触发依赖");
}

```

新建测试文件

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="../../dist/vue.js"></script>
  </head>
  <script>
    const { reactive } = Vue;
    const obj = reactive({
      name: "张三",
    });
    console.log(obj.name);
    obj.name = "李四";
  </script>
</html>
//控制台输出
track: 收集依赖
reactive.html:50 张三
effect.ts:17 trigger: 触发依赖

```

###### 构建effect

```js
/**
 * effect 函数
 * @param fn 执行方法
 * @returns 以 ReactiveEffect 实例为 this 的执行函数
 */
export function effect<T = any>(fn: () => T) {
  // 生成 ReactiveEffect 实例
  const _effect = new ReactiveEffect(fn);
  // 执行 run 函数
  _effect.run();
}

/**
 * 单例的，当前的 effect
 */
export let activeEffect: ReactiveEffect | undefined;
/**
 * 响应性触发依赖时的执行类
 */
export class ReactiveEffect<T = any> {
  constructor(public fn: () => T) {}
  run() {
    // 为 activeEffect 赋值
    activeEffect = this;
    // 执行 fn 函数
    return this.fn();
  }
}
```

这里的effect中实例化了ReactiveEffect，他的构造函数非常简单

- `public fn: () => T` 表示构造函数接收一个函数 `fn`，该函数没有参数且返回类型为 `T`。
- `public` 关键字表示 `fn` 是类的公共属性，可以直接通过实例访问。

然后就定义了run方法。

看下测试用例

```js
const { reactive, effect } = Vue;
const obj = reactive({
	name: "张三",
});
// 调用 effect 方法
effect(() => {
	document.querySelector("#app").innerText = obj.name;
});
```

effect中传入的fn是可以被正常执行的。

###### 依赖搜集触发

```js
type KeyToDepMap = Map<any, ReactiveEffect>;

/**
 * 收集所有依赖的 WeakMap 实例：
 * 1. `key`：响应性对象
 * 2. `value`：`Map` 对象
 * 1. `key`：响应性对象的指定属性
 * 2. `value`：指定对象的指定属性的 执行函数
 */
const targetMap = new WeakMap<any, KeyToDepMap>();
```

先指定搜集依赖的数据格式，就是targetMap，他的key使我们的响应式对象，value是一个map对象，其中key是指定的属性，value是执行函数fn。

响应性实际上就是当调用getter时搜集当前的fn函数，在后续触发setter时去执行fn函数。这个执行函数fn需要和对象以及对象的属性绑定，这就有个上面的targetMap。

接下来重新写一下track和trigger方法

```js
export function track(target: object, key: unknown) {
  // 如果当前不存在执行函数，则直接 return
  if (!activeEffect) return;
  // 尝试从 targetMap 中，根据 target 获取 map
  let depsMap = targetMap.get(target);
  // 如果获取到的 map 不存在，则生成新的 map 对象，并把该对象赋值给对应的 value
  if (!depsMap) {
    targetMap.set(target, (depsMap = new Map()));
  }
  //为指定 map，指定key 设置回调函数
  depsMap.set(key, activeEffect);
  // 临时打印
  console.log(targetMap);
}
/**
 * 触发依赖的方法
 * @param target WeakMap 的 key
 * @param key 代理对象的 key，当依赖被触发时，需要根据该 key 获取
 */
export function trigger(target: object, key?: unknown) {
  // 依据 target 获取存储的 map 实例
  const depsMap = targetMap.get(target);
  // 如果 map 不存在，则直接 return
  if (!depsMap) {
    return;
  }
  // 依据 key，从 depsMap 中取出 value，该 value 是一个 ReactiveEffect 类型的数据
  const effect = depsMap.get(key) as ReactiveEffect;
  // 如果 effect 不存在，则直接 return
  if (!effect) {
    return;
  }
  // 执行 effect 中保存的 fn 函数
  effect.fn();
}
```

当前的测试用例

```html
<script>
    const { reactive, effect } = Vue;
    const obj = reactive({
      name: "张三",
    });
    // 调用 effect 方法
    effect(() => {
      document.querySelector("#app").innerText = obj.name;
    });
    setTimeout(() => {
      obj.name = "李四";
    }, 2000);
</script>
```

可以看到2s后文本内容变成了李四。

上面的代码还有点问题，看下这个测试用例

```html
<body>
 	<div id="app">
       <p id="p1"></p>
       <p id="p2"></p>
 	</div>
</body>
<script>
 const { reactive, effect } = Vue
 const obj = reactive({
 	name: '张三'
 })
 // 调用 effect 方法
 effect(() => {
 	document.querySelector('#p1').innerText = obj.name
 })
 effect(() => {
 	document.querySelector('#p2').innerText = obj.name
 })
 setTimeout(() => {
 	obj.name = '李四'
 }, 2000);
</script>
```

这里的只有p2会发生变化。原因就在于这行代码

```js
export let activeEffect: ReactiveEffect | undefined;
```

activeEffect只有一个，可是测试用例里有两个fn，这里就需要将activeEffect改成一个数组了

新建`dep.ts`

```js
import { ReactiveEffect } from "./effect";
export type Dep = Set<ReactiveEffect>;

/**
 * 依据 effects 生成 dep 实例
 */
export const createDep = (effects?: ReactiveEffect[]): Dep => {
  const dep = new Set<ReactiveEffect>(effects) as Dep;
  return dep;
};

```

这里的dep就是上面的存放activeEffect的数组

修改下track方法

```js
export function track(target: object, key: unknown) {
  // 如果当前不存在执行函数，则直接 return
  if (!activeEffect) return;
  // 尝试从 targetMap 中，根据 target 获取 map
  let depsMap = targetMap.get(target);
  // 如果获取到的 map 不存在，则生成新的 map 对象，并把该对象赋值给对应的 value
  if (!depsMap) {
    targetMap.set(target, (depsMap = new Map()));
  }
  //为指定 map，指定key 设置回调函数
  // depsMap.set(key, activeEffect);
  let dep = depsMap.get(key);
  // 如果 dep 不存在，则生成一个新的 dep，并放入到 depsMap 中
  if (!dep) {
    depsMap.set(key, (dep = createDep()));
  }
  trackEffects(dep);
}

export function trackEffects(dep: Dep) {
  dep.add(activeEffect!);
}
```

这里在track时候，调用trackEffects将activeEffect保存起来

```js
export function trigger(target: object, key?: unknown) {
  // 依据 target 获取存储的 map 实例
  const depsMap = targetMap.get(target);
  // 如果 map 不存在，则直接 return
  if (!depsMap) {
    return;
  }
  // 依据指定的 key，获取 dep 实例
  let dep: Dep | undefined = depsMap.get(key);
  // dep 不存在则直接 return
  if (!dep) {
    return;
  }
  // 触发 dep
  triggerEffects(dep);
}
export function triggerEffects(dep: Dep) {
  // 把 dep 构建为一个数组
  const effects = Array.isArray(dep) ? dep : [...dep];
  // 依次触发
  for (const effect of effects) {
    triggerEffect(effect);
  }
}
/**
 * 触发指定的依赖
 */
export function triggerEffect(effect: ReactiveEffect) {
  effect.run();
}
```

在trigger时调用triggerEffects，将set转化为数组，依次触发activeEffect。这样就可以做到保存多个activeEffect了。

上述响应式基本已经完善了，但是还存在两个问题。当我们的target对象是基本对象时，比如字符串，就没有办法了，因为proxy对象的第一个参数必须是复杂对象；当对target对象进行解构，他也会丢失响应式。

这就需要用到vue3中的ref这个api了。

##### Ref

###### 基本用法

当我们在写vue3代码时，通过Ref申明的响应式都需要通过`.value`进行访问，

###### 源码阅读

当前的测试用例是这样

```html
<script>
const { ref, effect } = Vue
const obj = ref({
name: '张三',
})
// 调用 effect 方法
effect(() => {
document.querySelector('#app').innerText = obj.value.name
})
setTimeout(() => {
obj.value.name = '李四'
}, 2000)
</script>
```

打上断点，开始阅读源码。

ref方法定义在`packages/reactive/src/ref.ts`，函数里面返回了`createRef(value, false)`，其中value就是我们传入的对象， 在createRef返回了`new RefImpl(rawValue, shallow)`，这个RefImpl类就是实现ref的核心代码了。在其构造函数中有这样一行代码：`this._value = isShallow ? value : toReactive(value)`，这个isShallow 是false，在`createRef(value, false)`传入的，也就是说这会调用toReactive方法，这个toReactive方法也比较简单：

```js
export const toReactive = <T extends unknown>(value: T): T =>
  isObject(value) ? reactive(value) : value
```

isObject是判断当前传入的value是不是复杂对象，如果是就通过reactive进行包裹，如果不是就返回value。

紧接着RefImpl定义了get value和set value方法。这两个方法就是后续创造简单对象响应式数据的核心方法。

直接看3.2版本的。

```js
get value() {
    trackRefValue(this)
    return this._value
}

set value(newVal) {
    const useDirectValue =
          this.__v_isShallow || isShallow(newVal) || isReadonly(newVal)
    newVal = useDirectValue ? newVal : toRaw(newVal)
    if (hasChanged(newVal, this._rawValue)) {
        this._rawValue = newVal
        this._value = useDirectValue ? newVal : toReactive(newVal)
        triggerRefValue(this, newVal)
    }
}
```

get方法中会执行trackRefValue，然后执行trackEffects

```js
trackEffects(ref.dep || (ref.dep = createDep()), {
        target: ref,
        type: TrackOpTypes.GET,
        key: 'value'
      })
```

然后就是`dep.add(activeEffect!)`，和前面reactive中搜集依赖的流程一样。

set value方法中会执行`triggerRefValue`，然后执行triggerEffects

```js
triggerEffects(ref.dep, {
        target: ref,
        type: TriggerOpTypes.SET,
        key: 'value',
        newValue: newVal
      })
```

最终又会取执行`triggerEffect(effect, debuggerEventExtraInfo)`去触发依赖。



新建`ref.ts`

```js
import { createDep, Dep } from "./dep";
import { activeEffect, trackEffects } from "./effect";
import { toReactive } from "./reactive";
export interface Ref<T = any> {
  value: T;
}
/**
 * ref 函数
 * @param value unknown
 */
export function ref(value?: unknown) {
  return createRef(value, false);
}
/**
 * 创建 RefImpl 实例
 * @param rawValue 原始数据
 * @param shallow boolean 形数据，表示《浅层的响应性（即：只有 .value 是响应性的）》
 * @returns
 */
function createRef(rawValue: unknown, shallow: boolean) {
  if (isRef(rawValue)) {
    return rawValue;
  }
  return new RefImpl(rawValue, shallow);
}
class RefImpl<T> {
  private _value: T;
  public dep?: Dep = undefined;
  // 是否为 ref 类型数据的标记
  public readonly __v_isRef = true;
  constructor(value: T, public readonly __v_isShallow: boolean) {
    // 如果 __v_isShallow 为 true，则 value 不会被转化为 reactive 数据，即如果当前 v
    this._value = __v_isShallow ? value : toReactive(value);
  }
  /**
   * get语法将对象属性绑定到查询该属性时将被调用的函数。
   * 即：xxx.value 时触发该函数
   */
  get value() {
    trackRefValue(this);
    return this._value;
  }
  set value(newVal) {}
}
/**
 * 为 ref 的 value 进行依赖收集工作
 */
export function trackRefValue(ref) {
  if (activeEffect) {
    trackEffects(ref.dep || (ref.dep = createDep()));
  }
}
/**
 * 指定数据是否为 RefImpl 类型
 */
export function isRef(r: any): r is Ref {
  return !!(r && r.__v_isRef === true);
}

```

这里核心就是RefImpl，在构造函数中判断，如果是复杂对象，就通过toReactive方法将目标对象进行包裹，后续当我们通过.value访问时，就会调用trackRefValue方法，

看下测试案例

```html
<script>
    const { ref, effect } = Vue;
    const obj = ref({
      name: "张三",
    });
    // 调用 effect 方法
    effect(() => {
      document.querySelector("#app").innerText = obj.value.name;
    });
    setTimeout(() => {
      obj.value.name = "李四";
    }, 2000);
</script>
```

当ref穿一个简单对象时

```js
  。。。
  set value(newVal) {
    /**
     * newVal 为新数据
     * this._rawValue 为旧数据（原始数据）
     * 对比两个数据是否发生了变化
     */
    if (hasChanged(newVal, this._rawValue)) {
      // 更新原始数据
      this._rawValue = newVal;
      // 更新 .value 的值
      this._value = toReactive(newVal);
      // 触发依赖
      triggerRefValue(this);
    }
  }

export function triggerRefValue(ref) {
	if (ref.dep) {
		triggerEffects(ref.dep)
	}
}

export const hasChanged = (value: any, oldValue: any): boolean =>
  !Object.is(value, oldValue)


```





##### computed

###### 基本用法

看文档



###### 源码阅读

编写测试用例

```html
<script>
    const { reactive, computed, effect } = Vue
    const obj = reactive({
        name: '张三',
    })
    const computedObj = computed(() => {
        return '姓名：' + obj.name
    })
    effect(() => {
        document.querySelector('#app').innerHTML = computedObj.value
    })
    setTimeout(() => {
        obj.name = '李四'
    }, 2000)
</script>
```

打断点，查看源码

computed方法定义在`runtime-core/src/apiComputed.ts`中，

```js
const c = _computed(getterOrOptions, debugOptions, isInSSRComponentSetup)
```

核心代码就是执行了_computed方法，将结果c返回出去。





###### 代码实现

新建`computed.ts`

```js
import { isFunction } from "@vue/shared";
import { Dep } from "./dep";
import { ReactiveEffect } from "./effect";
import { trackRefValue, triggerRefValue } from "./ref";
/**
 * 计算属性类
 */
export class ComputedRefImpl<T> {
  public dep?: Dep = undefined;
  private _value!: T;
  public readonly effect: ReactiveEffect<T>;
  public readonly __v_isRef = true;
  public _dirty = true;
  constructor(getter) {
    this.effect = new ReactiveEffect(getter, () => {
      // 判断当前脏的状态，如果为 false，表示需要《触发依赖》
      if (!this._dirty) {
        // 将脏置为 true，表示
        this._dirty = true;
        triggerRefValue(this);
      }
    });
    this.effect.computed = this;
  }
  get value() {
    // 触发依赖
    trackRefValue(this);
    // 判断当前脏的状态，如果为 true ，则表示需要重新执行 run，获取最新数据
    if (this._dirty) {
      this._dirty = false;
      // 执行 run 函数
      this._value = this.effect.run()!;
    }
    // 返回计算之后的真实值
    return this._value;
  }
}

export function computed(getterOrOptions) {
  let getter;
  // 判断传入的参数是否为一个函数
  const onlyGetter = isFunction(getterOrOptions);
  if (onlyGetter) {
    // 如果是函数，则赋值给 getter
    getter = getterOrOptions;
  }
  const cRef = new ComputedRefImpl(getter);

  return cRef;
}

```

这里的computed同ref一样，都是返回一个实例，这里返回的事ComputedRefImpl的示例，在构造函数中实例化了ReactiveEffect，先传了一个getter，也就是我们使用计算属性传入的方法，第二个参数是一个匿名函数，也就称之为调度器，调度器中根据`_dirty`的状态来判断是否触发依赖；在ComputedRefImpl中也定义了一个get value方法，该方法中搜集了依赖，同时更新了`_dirty`的状态。

看下测试用例

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="../../dist/vue.js"></script>
  </head>
  <body>
    <div id="app"></div>
  </body>
  <script>
    const { reactive, computed, effect } = Vue;
    const obj = reactive({
      name: "张三1",
    });
    const computedObj = computed(() => {
      return "姓名：" + obj.name;
    });
    console.log(computedObj);
    effect(() => {
      document.querySelector("#app").innerHTML = computedObj.value;
    });
    setTimeout(() => {
      obj.name = "李四";
    }, 2000);
  </script>
</html>

```

2s后，视图发生了更改。



##### watch

源码位置在`runtime-core/src/apiWatch.ts`

















###### 核心api













##### 运行时







##### 编译器