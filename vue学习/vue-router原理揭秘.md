Vue Router 是 [Vue.js](https://vuejs.org/) 的官方路由。它与 Vue.js 核心深度集成，让用 Vue.js 构建单页应用变得轻而易举。功能包括：

- 嵌套路由映射
- 动态路由选择
- 模块化、基于组件的路由配置
- 路由参数、查询、通配符
- 展示由 Vue.js 的过渡系统提供的过渡效果
- 细致的导航控制
- 自动激活 CSS 类的链接
- HTML5 history 模式或 hash 模式
- 可定制的滚动行为
- URL 的正确编码

接下来了解下其基本用法

##### 基本用法

利用vue-cli生成项目，项目配置中选择vue-router，生成完成后运行`npm run serve`打开项目，在`src/router/index.js`中引入`VueRouter`，并且配置好路由对象：

```javascript
import Vue from 'vue'
import VueRouter from 'vue-router'
import pageA from '../views/pageA.vue'
import pageB from '../views/pageB.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'pageA',
    component: pageA
  },
  {
    path: '/pageB',
    name: 'pageB',
    component: pageB
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

```

`Vue.use(VueRouter)`用来注册路由插件，`Vue.use`会调用传入对象的install方法，routes为我们定义的路由规则，再通过`new VueRouter()`方法创建路由对象，最后导出router路由对象。

在view文件下定义两个组件:

```javascript
import pageA from '../views/pageA.vue'
import pageB from '../views/pageB.vue'
```

在`src/main.js`的vue构造函数中传入路由对象：

```javascript
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
```

这里会在vue实例上加上$route和$router两个属性，其中$route里面存储了一些路由规则参数等路由信息，$router上定义了路由的各种方法。

最后再`src/app.vue`中加入`<router-view/>`占位符，当匹配到对应的路由时会加载对应的组件来替换掉占位符。同时创建链接：

```javascript
<router-link to="/">Home</router-link> |
<router-link to="/pageB">About</router-link>
```

运行`npm run serve`点击按钮既可以看到路由切换。

###### 动态路由

在开发一些详情页时，可能需要这样的路由`detail/1`、`detail/2`，这就需要使用到动态路由，可以这样定义路由规则：

```javascript
{
    path: '/detail/:id',
    name: 'Detail',
    props:true,    
    component: () => import ('../views/Detail.vue')
}
```

这里定义组件时使用了路由懒加载，只有用户访问组件时才会加载该组件，接收id有两种方式：

- 通过`$route.params.id`
- 第二种通过props接收

```javascript
<template>
  <div class="about">
    <span>当前路由id：{{$route.params.id}}</span>
    <h2>{{id}}</h2>
    <h1>This is Detail</h1>
  </div>
</template>

<script>
export default {
  props:['id'],
  name:'Detail'
}
</script>
```



###### 嵌套路由

如同官网所说，一些应用程序的 UI 由多层嵌套的组件组成。在这种情况下，URL 的片段通常对应于特定的嵌套组件结构，例如：

```
/user/johnny/profile                     /user/johnny/posts
+------------------+                  +-----------------+
| User             |                  | User            |
| +--------------+ |                  | +-------------+ |
| | Profile      | |  +------------>  | | Posts       | |
| |              | |                  | |             | |
| +--------------+ |                  | +-------------+ |
+------------------+                  +-----------------+
```

这里定义一个layout组件，里面写上了公共的头部和尾部，其余部分需要路由匹配。

```javascript
//layout.vue
<template>
  <div>
    <h1>这里是头部</h1>
    <router-view></router-view>
    <h1>这里是底部</h1>
  </div>
</template>

<script>
export default {
  name:'layout',
}
</script>
```

这样定义下路由规则：

```javascript
{
    path: '/',
    component: layout,
    children:[
      {
        path: '/pageB',
        name: 'pageB',
        component: pageB
      },
      {
        path: '/pageA',
        name: 'pageA',
        component: pageA
      },
      {
        path: '/detail/:id',
        name: 'Detail',
        props:true,
        component: () => import ('../views/Detail.vue')
      }
    ]
  },
```

这样当路由匹配到pageB或者pageA时就能加载layout组件内的东西了。



###### 编程式导航

跳转路由除了上面的`<router-link to="/">Home</router-link> `，在$router上定义了其他的方法：

- $route.push()

  这个方法可以通过路由跳转，

  ```javascript
  this.$router.push('/pageA')
  ```

  也可以通过定义路由规则时的name跳转，这种方式可以加个params给路由传参

  ```javascript
  this.$router.push({name:'Detail',params:{
     id:15
  }})
  ```

- $route.replace()

  这个方法同样也可以实现路由跳转

  ```javascript
  this.$router.replace('/pageA')
  ```

  区别不同的就是replace方法是在导航时不会向 history 添加新记录，正如它的名字所暗示的那样——它取代了当前的条目。 

  同样我们也可以返回上一条历史记录：

  ```javascript
  this.$router.go(-1)
  ```

  或者是

  ```javascript
  this.$router.back()
  ```

  ##### 

###### 路由守卫

-  router.beforeEach  全局前置守卫

  接受两个参数to和from，to是即将进入的目标，from是导航离开的路由。

  如果返回false，表明取消本次导航，如果导航地址更改了，会重定向到from路由对应的地址；如果返回的是一个路由地址，就相当于调用router.push一样，跳转一个新的路由。

- router.beforeResolve  全局解析守卫， 这和 `router.beforeEach` 类似，因为它在 每次导航时都会触发，但是确保在导航被确认之前，同时在所有组件内守卫和异步路由组件被解析之后，解析守卫就被正确调用。
- router.afterEach() 全局后置钩子， 可以做一些分析、更改页面标题、声明页面等辅助功能 ，无法更改路由。
- beforeEnter（），这个是路由独享的守卫，可以再配置路由规则时定义，会在路由进入时触发
- beforeRouteEnter（），beforeRouteUpdate（），beforeRouteLeave（）这三个都是组件内的守卫，用法基本类似。

###### Hash模式和History模式

在我们利用VueRouter创建路由组建时，有一个mode字段，这个就是申明我们的路由以何种模式来运行的，

```javascript
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
```

这里使用的是history模式来创建路由，还可以使用`mode:hash`来创建hash模式的路由，这两种模式不管表现形式还是原理差距都很大，接下来一一介绍下：

- hash

  监听浏览器地址hash值变化，执行相应的js切换网页 。使用window.location.hash属性及窗口的onhashchange事件，可以实现监听浏览器地址hash值变化。其主要有以下几个特点：

  - hash指的是地址中#号以及后面的字符，也称为散列值。hash也称作锚点，本身是用来做页面跳转定位的。如[http://localhost/index.html#abc，这里的#abc就是hash；]
  - 散列值是不会随请求发送到服务器端的，所以改变hash，不会重新加载页面；
  - 监听 window 的 hashchange 事件，当散列值改变时，可以通过 location.hash 来获取和设置hash值；
  - location.hash值的变化会直接反应到浏览器地址栏；

  

- history

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

  而history模式还有一个问题需要注意下，单页面应用实际上就是我们在第一次进入页面时，向服务器发送请求，获得数据，后续的路由更改并不会向服务器发送请求，而是通过路由匹配对应的组件来实现页面更新，而history部署在不同的服务器上，需要配置下服务器，不然就会请求一个不存在的地址并不会匹配到404组件，而是一个会返回一个404的状态码，用一个例子更加情绪的描述下问题：

  首先将上述项目运行`npm run build`打包，新建一个web目录，将打包的dist目录下的文件全部拖入到改web文件下，新建一个fuwu目录，安装两个模块`express`和`connect-history-api-fallback`，简单的搭建一个静态服务器

  ```javascript
  //app.js
  const path = require('path')
  // 导入处理 history 模式的模块
  const history = require('connect-history-api-fallback')
  // 导入 express
  const express = require('express')
  
  const app = express()
  // 注册处理 history 模式的中间件
  // app.use(history())
  // 处理静态资源的中间件，网站根目录 ../web
  app.use(express.static(path.join(__dirname, '../web')))
  
  // 开启服务器，端口是 3000
  app.listen(3001, () => {
    console.log('服务器开启，端口：3001')
  })
  
  ```

  `node app.js`启动下这个服务，就可以看到我们的项目了，点击按钮也能跳转对应的路由，在路由规则中添加一个404的路由：

  ```javascript
  {
      path: '*',
      component: nothing
  },
  ```

  当我们在导航栏中输入`pageB1`，这是一个不存在的路由，并不会命中nothing组件，而是直接返回一个404的状态码，这时就需要在我们的服务器中添加一个中间件，`app.use(history())`，再重新启动下我们的服务器，再次输入不存在的路径时，就会匹配我们的nothing组件了。

  如果是nginx服务的话，就需要修改下conf/nginx.conf文件：

  ```javascript
  location / {
  	root html;
  	index index.html index.htm;
  	#新添加内容
  	#尝试读取$uri(当前请求的路径)，如果读取不到读取$uri/这个文件夹下的首页
  	#如果都获取不到返回根目录中的 index.html
  	try_files $uri $uri/ /index.html;
  }
  
  ```

  

##### 手写vue-router

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

 [代码地址](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fjinxudong996%2Fblog%2Ftree%2Fmain%2Fvue%E5%AD%A6%E4%B9%A0%2Fcode%2Fvue-router%2Froute) 