## vue源码学习

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

  在vue项目的main.js文件中，都会有一个实例化Vue的过程，即new Vue({...})，而Vue 一般是个构造函数，这个构造函数在src/core/instance/index.js文件中。

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

  这里先通过运算符instanceof判断是不是Vue的一个实例，不是的话就抛出一个警告，随后调用的_init()方法，这里通过this调用，构造函数的this应该是指向新实例的，可以断定这个_init()方法在Vue的原型上。在src/core/instance/init.js中定义了这个原型方法：

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

  这里通过initMixin()方法，传入Vue构造函数，在initmixin()内定义Vue.prototype._init。Vue这种大型框架考虑的东西比较多，有着各种繁琐的情况判断，核心就是一些初始化代码。

- Vue实例挂载

  

- 虚拟dom

  