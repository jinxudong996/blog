vue源码学习

- 源码调试

  直接从github上拉下代码，目前看的是2.6版本的。然后执行npm install安装下所需要的插件，打开package.json文件，

  ```JavaScript
  "scripts": {
      "dev": "rollup -w -c scripts/config.js --environment TARGET:web-full-dev",
      "dev:cjs": "rollup -w -c scripts/config.js --environment TARGET:web-runtime-cjs-dev",
      "dev:esm": "rollup -w -c scripts/config.js --environment TARGET:web-runtime-esm",
      "dev:test": "karma start test/unit/karma.dev.config.js",
      "dev:ssr": "rollup -w -c scripts/config.js --environment TARGET:web-server-renderer",
      "dev:compiler": "rollup -w -c scripts/config.js --environment TARGET:web-compiler ",
      "dev:weex": "rollup -w -c scripts/config.js --environment TARGET:weex-framework",
      "dev:weex:factory": "rollup -w -c scripts/config.js --environment TARGET:weex-factory",
      "dev:weex:compiler": "rollup -w -c scripts/config.js --environment TARGET:weex-compiler ",
  ```

  其中dev里的命令分别是

  > rollup   vue源码使用的rollup打包的
  >
  > -w      监控所有的代码  当源码发生变化时 重新打包
  >
  > -c    设置配置文件   scripts/config.js
  >
  > --environment  设置环境变量  通过环境变量来打成不同的包

  这里有一个小坑，直接运行npm run dev会报错，网上找了些资料说是 [**rollup-plugin-alias.js**](https://gist.github.com/zhoukekestar/97e1b3c8ad129d8740668b5b44f97d18#file-rollup-plugin-alias-js) 这个文件只支持win32的

  ```JavaScript
  // ------------line 13 ------------
  const VOLUME = /^([A-Z]:)/i; // ignore case
  const IS_WINDOWS = os.platform() === 'win32';
  ```

  找到上述的js替换下，就能解决。[解决方案](https://github.com/vuejs/vue/issues/2771)

  打包完成后就可以看到dist下更新的文件，此时就可以去examples文件下进行源码调试。

  以examples文件下的grid来举例，在index.html中的script标签中，将vue链接改为刚打的包

  ```html
  <script src="../../dist/vue.js"></script>
  ```

  随后在浏览器中打开该文件，审查元素，在grid.js中的实例化vue处设置断点，单步进入，第一个文件就是`core/instance/index.js`，判断环境变量

  ![](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1633427366353.png)

  接下来就可以进行后续的源码学习。

- 框架结构

  vue的源码基本都在src目录下面。

  ```JavaScript
  src
  ├── compiler        # 编译相关 
  ├── core            # 核心代码 
  ├── platforms       # 不同平台的支持
  ├── server          # 服务端渲染
  ├── sfc             # .vue 文件解析
  ├── shared          # 共享代码
  ```

- new Vue（）发生了什么

  在vue项目的main.js文件中，都会有一个实例化Vue的过程，即new Vue({...})，而Vue 一般是个构造函数，这个构造函数在`src/core/instance/index.js`文件中。

  ```JavaScript
  function Vue (options) {
    if (process.env.NODE_ENV !== 'production' &&
      !(this instanceof Vue)
    ) {
      warn('Vue is a constructor and should be called with the `new` keyword')
    }
    this._init(options)
  }
  ```

  这里先通过运算符instanceof判断是不是Vue的一个实例，不是的话就抛出一个警告，随后调用的_init()方法，这里通过this调用，构造函数的this是指向新实例的，可以断定这个_init()方法在Vue的原型上。在`src/core/instance/init.js`中定义了这个原型方法：

  ```JavaScript
  export function initMixin (Vue: Class<Component>) {
    Vue.prototype._init = function (options?: Object) {
      const vm: Component = this
      // a uid
      vm._uid = uid++
  
      let startTag, endTag
      /* istanbul ignore if */
      if (process.env.NODE_ENV !== 'production' && config.performance && mark) {
        startTag = `vue-perf-start:${vm._uid}`
        endTag = `vue-perf-end:${vm._uid}`
        mark(startTag)
      }
  
      // a flag to avoid this being observed
      vm._isVue = true
      // merge options
      if (options && options._isComponent) {
        // optimize internal component instantiation
        // since dynamic options merging is pretty slow, and none of the
        // internal component options needs special treatment.
        initInternalComponent(vm, options)
      } else {
        vm.$options = mergeOptions(
          resolveConstructorOptions(vm.constructor),
          options || {},
          vm
        )
      }
      /* istanbul ignore else */
      if (process.env.NODE_ENV !== 'production') {
        initProxy(vm)
      } else {
        vm._renderProxy = vm
      }
      // expose real self
      vm._self = vm
      initLifecycle(vm)
      initEvents(vm)
      initRender(vm)
      callHook(vm, 'beforeCreate')
      initInjections(vm) // resolve injections before data/props
      initState(vm)
      initProvide(vm) // resolve provide after data/props
      callHook(vm, 'created')
  
      /* istanbul ignore if */
      if (process.env.NODE_ENV !== 'production' && config.performance && mark) {
        vm._name = formatComponentName(vm, false)
        mark(endTag)
        measure(`vue ${vm._name} init`, startTag, endTag)
      }
  
      if (vm.$options.el) {
        vm.$mount(vm.$options.el)
      }
    }
  }
  ```

  这里通过initMixin()方法，传入Vue构造函数，在initmixin()内定义Vue.prototype._init。核心就是一些初始化代码， 合并配置，初始化生命周期，初始化事件中心，初始化渲染，初始化 data、props、computed、watcher 等等。 最后判断如果有el属性，就执行$mount()方法， 这个方是把模板渲染成最终的 DOM。通过断点，这个方法定义在`src/platforms/web/entry-runtime-with-compiler.js`里

   

  ```JavaScript
  const mount = Vue.prototype.$mount
  Vue.prototype.$mount = function (
    el?: string | Element,
    // 非ssr情况下为 false，ssr 时候为true
    hydrating?: boolean
  ): Component {
    // 获取 el 对象
    el = el && query(el)
  
    /* istanbul ignore if */
    // el 不能是 body 或者 html
    if (el === document.body || el === document.documentElement) {
      process.env.NODE_ENV !== 'production' && warn(
        `Do not mount Vue to <html> or <body> - mount to normal elements instead.`
      )
      return this
    }
  
    const options = this.$options
    // resolve template/el and convert to render function
    // 把 template/el 转换成 render 函数
    if (!options.render) {
      let template = options.template
      // 如果模板存在
      if (template) {
        if (typeof template === 'string') {
          // 如果模板是 id 选择器
          if (template.charAt(0) === '#') {
            // 获取对应的 DOM 对象的 innerHTML
            template = idToTemplate(template)
            /* istanbul ignore if */
            if (process.env.NODE_ENV !== 'production' && !template) {
              warn(
                `Template element not found or is empty: ${options.template}`,
                this
              )
            }
          }
        } else if (template.nodeType) {
          // 如果模板是元素，返回元素的 innerHTML
          template = template.innerHTML
        } else {
          if (process.env.NODE_ENV !== 'production') {
            warn('invalid template option:' + template, this)
          }
          // 否则返回当前实例
          return this
        }
      } else if (el) {
        // 如果没有 template，获取el的 outerHTML 作为模板
        template = getOuterHTML(el)
      }
      if (template) {
        /* istanbul ignore if */
        if (process.env.NODE_ENV !== 'production' && config.performance && mark) {
          mark('compile')
        }
        // 把 template 转换成 render 函数
        const { render, staticRenderFns } = compileToFunctions(template, {
          outputSourceRange: process.env.NODE_ENV !== 'production',
          shouldDecodeNewlines,
          shouldDecodeNewlinesForHref,
          delimiters: options.delimiters,
          comments: options.comments
        }, this)
        options.render = render
        options.staticRenderFns = staticRenderFns
  
        /* istanbul ignore if */
        if (process.env.NODE_ENV !== 'production' && config.performance && mark) {
          mark('compile end')
          measure(`vue ${this._name} compile`, 'compile', 'compile end')
        }
      }
    }
    // 调用 mount 方法，渲染 DOM
    return mount.call(this, el, hydrating)
  }
  ```

  这里把原型上的$mount方法保存到了一个变量mount里，接下来重写了原型上的$mount方法。

  在重写的$mount方法里先对el进行校验，vue不能够挂载在html和doby这样的根节点上面，紧接着又判断了如果实例化vue的参数里有render函数，就直接调用原先原型上的$mount方法渲染dom，如果没有render函数，就将el或者template字符串通过compileToFunctions方法转化为render方法。

  原先原型上的$mount方法定义在`src/platforms/web/runtime/index.js`里的，

  ```JavaScript
  Vue.prototype.$mount = function (
    el?: string | Element,
    hydrating?: boolean
  ): Component {
    el = el && inBrowser ? query(el) : undefined
    return mountComponent(this, el, hydrating)
  }
  ```

  实际上也是调用了在·定义的mountComponent方法

  ```JavaScript
  export function mountComponent (
    vm: Component,
    el: ?Element,
    hydrating?: boolean
  ): Component {
    vm.$el = el
    if (!vm.$options.render) {
      vm.$options.render = createEmptyVNode
      if (process.env.NODE_ENV !== 'production') {
        /* istanbul ignore if */
        if ((vm.$options.template && vm.$options.template.charAt(0) !== '#') ||
          vm.$options.el || el) {
          warn(
            'You are using the runtime-only build of Vue where the template ' +
            'compiler is not available. Either pre-compile the templates into ' +
            'render functions, or use the compiler-included build.',
            vm
          )
        } else {
          warn(
            'Failed to mount component: template or render function not defined.',
            vm
          )
        }
      }
    }
    callHook(vm, 'beforeMount')
  
    let updateComponent
    /* istanbul ignore if */
    if (process.env.NODE_ENV !== 'production' && config.performance && mark) {
      updateComponent = () => {
        const name = vm._name
        const id = vm._uid
        const startTag = `vue-perf-start:${id}`
        const endTag = `vue-perf-end:${id}`
  
        mark(startTag)
        const vnode = vm._render()
        mark(endTag)
        measure(`vue ${name} render`, startTag, endTag)
  
        mark(startTag)
        vm._update(vnode, hydrating)
        mark(endTag)
        measure(`vue ${name} patch`, startTag, endTag)
      }
    } else {
      updateComponent = () => {
        vm._update(vm._render(), hydrating)
      }
    }
  
    // we set this to vm._watcher inside the watcher's constructor
    // since the watcher's initial patch may call $forceUpdate (e.g. inside child
    // component's mounted hook), which relies on vm._watcher being already defined
    new Watcher(vm, updateComponent, noop, {
      before () {
        if (vm._isMounted && !vm._isDestroyed) {
          callHook(vm, 'beforeUpdate')
        }
      }
    }, true /* isRenderWatcher */)
    hydrating = false
  
    // manually mounted instance, call mounted on self
    // mounted is called for render-created child components in its inserted hook
    if (vm.$vnode == null) {
      vm._isMounted = true
      callHook(vm, 'mounted')
    }
    return vm
  }
  ```

  这个函数里主要就是定义了一个updateComponent 方法， 在此方法中调用 `vm._render` 方法先生成虚拟 Node，最终调用 `vm._update` 更新 DOM。 随后再渲染一个watcher，在回调中调用updateComponent 方法。这里核心的方法就是_render方法，定义在 `src/core/instance/render.js` ，

  ```JavaScript
  Vue.prototype._render = function (): VNode {
      const vm: Component = this
      const { render, _parentVnode } = vm.$options
  
      if (_parentVnode) {
        vm.$scopedSlots = normalizeScopedSlots(
          _parentVnode.data.scopedSlots,
          vm.$slots,
          vm.$scopedSlots
        )
      }
  
      // set parent vnode. this allows render functions to have access
      // to the data on the placeholder node.
      vm.$vnode = _parentVnode
      // render self
      let vnode
      try {
        // There's no need to maintain a stack because all render fns are called
        // separately from one another. Nested component's render fns are called
        // when parent component is patched.
        currentRenderingInstance = vm
        vnode = render.call(vm._renderProxy, vm.$createElement)
      } catch (e) {
        handleError(e, vm, `render`)
        // return error render result,
        // or previous vnode to prevent render error causing blank component
        /* istanbul ignore else */
        if (process.env.NODE_ENV !== 'production' && vm.$options.renderError) {
          try {
            vnode = vm.$options.renderError.call(vm._renderProxy, vm.$createElement, e)
          } catch (e) {
            handleError(e, vm, `renderError`)
            vnode = vm._vnode
          }
        } else {
          vnode = vm._vnode
        }
      } finally {
        currentRenderingInstance = null
      }
      // if the returned array contains only a single node, allow it
      if (Array.isArray(vnode) && vnode.length === 1) {
        vnode = vnode[0]
      }
      // return empty vnode in case the render function errored out
      if (!(vnode instanceof VNode)) {
        if (process.env.NODE_ENV !== 'production' && Array.isArray(vnode)) {
          warn(
            'Multiple root nodes returned from render function. Render function ' +
            'should return a single root node.',
            vm
          )
        }
        vnode = createEmptyVNode()
      }
      // set parent
      vnode.parent = _parentVnode
      return vnode
    }
  ```

  这里通过call方法执行了render函数，并将vm.$createElement当做参数传入，一般使用render函数都是

  ```javascript
  render: function (createElement) {
    return createElement('div', {
       attrs: {
          id: 'app'
        },
    }, this.message)
  }
  ```

   可以看到，`render` 函数中的 createElement 方法就是 vm.$createElement 方法： 

  ```javascript
  // 对编译生成的 render 进行渲染的方法
  vm._c = (a, b, c, d) => createElement(vm, a, b, c, d, false)
  // normalization is always applied for the public version, used in
  // user-written render functions.
  // 对手写 render 函数进行渲染的方法
  vm.$createElement = (a, b, c, d) => createElement(vm, a, b, c, d, true)
  ```

   vm.$createElement 方法定义是在执行 initRender 方法的时候，可以看到除了 vm.$createElement 方法，还有一个 vm._c 方法，它是被模板编译成的 render 函数使用，而 vm.$createElement 是用户手写 render 方法使用的， 这俩个方法支持的参数相同，并且内部都调用了 createElement 方法。 

   vm._render 最终是通过执行 createElement 方法并返回的是 `vnode`，它是一个虚拟 Node 。

   真正的 DOM 元素是非常庞大的，因为浏览器的标准就把 DOM 设计的非常复杂。当我们频繁的去做 DOM 更新，会产生一定的性能问题 。而 Virtual DOM 就是用一个原生的 JS 对象去描述一个 DOM 节点，所以它比创建一个 DOM 的代价要小很多。在 Vue.js 中，Virtual DOM 是用 VNode 这么一个 Class 去描述，它是定义在 src/core/vdom/vnode.js 中的。  Vue.js 中 Virtual DOM 是借鉴了一个开源库 [snabbdom](https://github.com/snabbdom/snabbdom) 的实现，然后加入了一些 Vue.js 特色的东西。

   其实 VNode 是对真实 DOM 的一种抽象描述，它的核心定义无非就几个关键属性，标签名、数据、子节点、键值等，其它属性都是用来扩展 VNode 的灵活性以及实现一些特殊 feature 的。由于 VNode 只是用来映射到真实 DOM 的渲染，不需要包含操作 DOM 的方法，因此它是非常轻量和简单的。  这个库后续有时间研究下。

  上述利用 createElement 方法创建 VNode，它定义在 src/core/vdom/create-element.js 中 ，

  ```JavaScript
  export function createElement (
    context: Component,
    tag: any,
    data: any,
    children: any,
    normalizationType: any,
    alwaysNormalize: boolean
  ): VNode | Array<VNode> {
    if (Array.isArray(data) || isPrimitive(data)) {
      normalizationType = children
      children = data
      data = undefined
    }
    if (isTrue(alwaysNormalize)) {
      normalizationType = ALWAYS_NORMALIZE
    }
    return _createElement(context, tag, data, children, normalizationType)
  }
  ```

  createElement函数主要还是执行了 _createElement 方法，它的工作就是对参数进行了一些处理，随后调用真正创建 VNode 的函数 _createElement

  ```javascript
  export function _createElement (
    context: Component,
    tag?: string | Class<Component> | Function | Object,
    data?: VNodeData,
    children?: any,
    normalizationType?: number
  ): VNode | Array<VNode> {
    if (isDef(data) && isDef((data: any).__ob__)) {
      process.env.NODE_ENV !== 'production' && warn(
        `Avoid using observed data object as vnode data: ${JSON.stringify(data)}\n` +
        'Always create fresh vnode data objects in each render!',
        context
      )
      return createEmptyVNode()
    }
    // object syntax in v-bind
    if (isDef(data) && isDef(data.is)) {
      tag = data.is
    }
    if (!tag) {
      // in case of component :is set to falsy value
      return createEmptyVNode()
    }
    // warn against non-primitive key
    if (process.env.NODE_ENV !== 'production' &&
      isDef(data) && isDef(data.key) && !isPrimitive(data.key)
    ) {
      if (!__WEEX__ || !('@binding' in data.key)) {
        warn(
          'Avoid using non-primitive value as key, ' +
          'use string/number value instead.',
          context
        )
      }
    }
    // support single function children as default scoped slot
    if (Array.isArray(children) &&
      typeof children[0] === 'function'
    ) {
      data = data || {}
      data.scopedSlots = { default: children[0] }
      children.length = 0
    }
    if (normalizationType === ALWAYS_NORMALIZE) {
      children = normalizeChildren(children)
    } else if (normalizationType === SIMPLE_NORMALIZE) {
      children = simpleNormalizeChildren(children)
    }
    let vnode, ns
    if (typeof tag === 'string') {
      let Ctor
      ns = (context.$vnode && context.$vnode.ns) || config.getTagNamespace(tag)
      if (config.isReservedTag(tag)) {
        // platform built-in elements
        vnode = new VNode(
          config.parsePlatformTagName(tag), data, children,
          undefined, undefined, context
        )
      } else if (isDef(Ctor = resolveAsset(context.$options, 'components', tag))) {
        // component
        vnode = createComponent(Ctor, data, context, children, tag)
      } else {
        // unknown or unlisted namespaced elements
        // check at runtime because it may get assigned a namespace when its
        // parent normalizes children
        vnode = new VNode(
          tag, data, children,
          undefined, undefined, context
        )
      }
    } else {
      // direct component options / constructor
      vnode = createComponent(tag, data, context, children)
    }
    if (Array.isArray(vnode)) {
      return vnode
    } else if (isDef(vnode)) {
      if (isDef(ns)) applyNS(vnode, ns)
      if (isDef(data)) registerDeepBindings(data)
      return vnode
    } else {
      return createEmptyVNode()
    }
  }
  ```

  

- Vue实例挂载

  

- 虚拟dom

  