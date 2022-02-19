手写vue-router

#### 前言

单页面应用利用了JavaScript动态变换网页内容，避免了页面重载；路由则提供了浏览器地址变化，网页内容也跟随变化，两者结合起来则为我们提供了体验良好的单页面web应用。 

目前前端实现路由有两种模式：Hash模式和history模式

##### Hash模式

 监听浏览器地址hash值变化，执行相应的js切换网页 。使用window.location.hash属性及窗口的onhashchange事件，可以实现监听浏览器地址hash值变化。其主要有以下几个特点：

- hash指的是地址中#号以及后面的字符，也称为散列值。hash也称作锚点，本身是用来做页面跳转定位的。如http://localhost/index.html#abc，这里的#abc就是hash；
- 散列值是不会随请求发送到服务器端的，所以改变hash，不会重新加载页面；
- 监听 window 的 hashchange 事件，当散列值改变时，可以通过 location.hash 来获取和设置hash值；
- location.hash值的变化会直接反应到浏览器地址栏；



##### history模式

利用history API实现url地址改变，根据当前路由地址找到对应组件重新渲染。 window.history 属性指向 History 对象，它表示当前窗口的浏览历史。当发生改变时，只会改变页面的路径，不会刷新页面 。而且History 对象保存了当前窗口访问过的所有页面网址。通过 history.length 可以得出当前窗口一共访问过几个网址。浏览器工具栏的前进和后退按钮，其实就是对History对象进行操作。

History主要有两个属性：

- History.length:当前窗口访问过的网址数量
- History.state:History堆栈最上层的状态值

History对象主要由五个静态方法：

- History.back()： 移动到上一个网址，等同于点击浏览器的后退键。对于第一个访问的网址，该方法无效果 

- History.forward()： 移动到下一个网址，等同于点击浏览器的前进键。对于最后一个访问的网址，该方法无效果。 

- History.go()： 接受一个整数作为参数，以当前网址为基准，移动到参数指定的网址。如果参数超过实际存在的网址范围，该方法无效果；如果不指定参数，默认参数为`0`，相当于刷新当前页面。 

- History.pushState()： 该方法用于在历史中添加一条记录，不会刷星页面，会导致History对象和地址栏发生变化，接受三个参数：

  - object，一个对象， 通过 pushState 方法可以将该对象内容传递到新页面中。如果不需要这个对象，此处可以填 null。 
  - title，指标题，几乎没有浏览器支持该参数，传一个空字符串比较安全。 
  - url， 新的网址，必须与当前页面处在同一个域。 

- History.replaceState()： 该方法用来修改 History 对象的当前记录，用法与 pushState() 方法一样 

  

##### popstate事件

每当 history 对象出现变化时，就会触发 popstate 事件，该事件主要有以下特点：

- 仅仅调用pushState()、replaceState()并不会触发该事件
-  有用户点击浏览器倒退按钮和前进按钮，或者使用 JavaScript 调用`History.back()`、`History.forward()`、`History.go()`方法时才会触发 
-  事件只针对同一个文档，如果浏览历史的切换，导致加载不同的文档，该事件也不会触发 
- 页面第一次加载的时候，浏览器不会触发`popstate`事件。

history 有一个缺点就是当改变页面地址后，强制刷新浏览器时，（如果后端没有做准备的话）会报错，因为刷新是拿当前地址去请求服务器的，如果服务器中没有相应的响应，会出现 404 页面。 



#### 模拟实现

##### 基本用法

可以去vue官网中查看其使用方法：

```javascript
vue.use(VueRouter)

const router = new VueRouter({
	routes:[
		{name:'home',path:'/',component:homeComponent}
	]
})

new Vue({
	router,
	render:h=>(App)
}).$mount('#app')
```

vue-router是通过vue.use()来注册插件的，该方法接受函数或者对象，如果是对象的话就会调用它的install方法；如果是函数就会执行该函数。

##### 代码编写

首先安装vue-cli，使用脚手架创建一个vue项目，准备在这个项目中验证我们的路由系统。在项目的根目录下新建vue-router目录，目录下新建index.js，首先编写下install方法：

```javascript
let _Vue = null
export default class VueRouter {
    static install(Vue){
        //1 判断当前插件是否被安装
        if(VueRouter.install.installed){
            return;
        }
        VueRouter.install.installed = true
        //2 把Vue的构造函数记录在全局
        _Vue = Vue
        //3 把创建Vue实例传入的router对象注入到Vue实例
        _Vue.mixin({
            beforeCreate(){
                if(this.$options.router){
                    _Vue.prototype.$router = this.$options.router
                }
               
            }
        })
    }

}
```

这里首先判断了当前插件是否被安装，用一个变量记录，如果被安装了就不在走后续流程；随后将install函数中传入的vue实例记录到全局，后续需要用到实例上的很多方法；最后将创建Vue实例时传入的router对象挂载到Vue实例，这里借用了混入方法，在beforeCreate()钩子函数里做一下判断，只给vue实例去挂载，而组件就不需要了。

接着编写下类的构造器：

```javascript
constructor(options){
    this.options = options
    this.routeMap = {}
    // observable
    this.data = _Vue.observable({
        current:"/"
    })
    this.init()
}
```

该构造器挂在了三个属性到路由实例上，options就是传入的route数组，包含路由和组件，routeMap就是路由与对应组件的依赖，而data是由_Vue.observable创建的响应式对象，里面的current代表当前路由。

紧接着解析下传入的options，将对应的路由和组件存入routeMap

```javascript
createRouteMap(){
    //遍历所有的路由规则 吧路由规则解析成键值对的形式存储到routeMap中
    this.options.routes.forEach(route => {
        this.routeMap[route.path] = route.component
    });
}
```

接下来就开始编写route-link组件和route-view组件

```javascript
initComponent(Vue){
    Vue.component("router-link",{
        props:{
            to:String
        },
        render(h){
            return h("a",{
                attrs:{
                    href:this.to
                },
                on:{
                    click:this.clickhander
                }
            },[this.$slots.default])
        },
        methods:{
            clickhander(e){
                history.pushState({},"",this.to)
                this.$router.data.current=this.to
                e.preventDefault()
            }
        }
        // template:"<a :href='to'><slot></slot><>"
    })
    const self = this
    Vue.component("router-view",{
        render(h){
            // self.data.current
            const cm=self.routeMap[self.data.current]
            return h(cm)
        }
    })
}
```

编写组件时使用render函数，render函数接受一个函数作为参数，根据该函数来渲染成虚拟dom。该函数接受三个参数，第一个创建元素的选择器；第二个设置元素的属性，这里通过attrs设置了元素的href属性和通过on绑定了的click事件；第三个设置元素的内容，这里是获取了默认插槽的内容。

在最后监听了popstate事件，根据前言，点击浏览器的前进和后退就会触发该函数，在回调中设置了data中的current，由于data是响应式数据，一旦更改就会重新更新视图。

```javascript
initEvent(){
    //
    window.addEventListener("popstate",()=>{
        this.data.current = window.location.pathname
    })
}
```

[代码地址](https://github.com/jinxudong996/blog/tree/main/vue%E5%AD%A6%E4%B9%A0/code/vue-router/route)

吐槽下typeora，记得写完保存了，上传掘金时发现只有一半，找都找不回来，大半夜的重新写。。。

