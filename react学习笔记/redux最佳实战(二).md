##### 基础回顾

redux和vuex蛮像的，都是有一个state数据仓库，通过dispatch触发action来调用reducer去更改state，store会订阅subscribe去更新视图。

如果再react中使用的话，就会用到react-redux，这个包会导出一个Provider组件和content方法，Provider会注册store实例，其中所有的子组件都能引用。content方法会订阅store，当store中的数据更改时会重新渲染组件。同时也会将store中的state和dispatch方法隐射给props。content这个方法接受两个参数，第一个是将state隐射到props的函数，第二个

redux-thunk就是对redux做一个异步操作，他将action返回一个函数，函数的参数就是dispatch，在异步操作中dispatch其他的action将返回的数据存储到state里。

react-saga可以将异步操作从action Creator文件中抽离出来，放到一个单独的文件中。

![1665970185000](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1665970185000.png)

会导出一个gengerator函数







##### 购物车案例





##### 手写redux