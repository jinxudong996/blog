koa学习笔记

>  Koa 是一个新的 web 框架，由 Express 幕后的原班人马打造， 致力于成为 web 应用和 API 开发领域中的一个更小、更富有表现力、更健壮的基石。 通过利用 async 函数，Koa 帮你丢弃回调函数，并有力地增强错误处理。 Koa 并没有捆绑任何中间件， 而是提供了一套优雅的方法，帮助您快速而愉快地编写服务端应用程序。 

- koa主要通过async函数来处理异步，丢弃回调函数
- koa提供了ctx上下文
- koa没有捆绑任何中间件

##### 基本使用

```javascript
const koa = require('koa')

const app = new koa()

app.use(ctx => {
    ctx.body = 'hello koa'
})

app.listen(3000,() => {
    console.log('koa....')
})
```

- 上下文

  koa context将node的request和response对象封装到单个对象中，为编写web应用程序和api提供了许多有用的方法。

  每个请求都会创建一个context对象，在中间件中接收使用。

  ```javascript
  app.use(ctx => {
  	ctx //context
  	ctx.request// koa request
  	ctx.response// koa response
  })
  ```

  

- 路由

  koa中并没有集成路由，得自己一个个判断

  ```javascript
  app.use(ctx => {
      console.log(ctx)
      const path = ctx.path
      if(path == '/'){
          ctx.body = 'hello koa /'
      } else if(path == '/about'){
          ctx.body = 'hello koa about'
      }else{
          ctx.body = 'hello koa 404'
      }
      
  })
  ```

  如果想使用express风格的路由，需要加载一个模块`@koa/router`

  ```javascript
  const koa = require('koa')
  const router = require('@koa/router')
  
  const app = new koa()
  const route = new router()
  
  route.get('/', ctx => {
      ctx.body = 'hello koa /'
  })
  
  route.get('/about', ctx => {
      ctx.body = 'hello koa about'
  })
  
  app.use(route.routes())
  
  app.listen(3000,() => {
      console.log('koa....')
  })
  ```

- 中间件栈

  koa最大的特色，也是最重要的一个设计，就是中间件。

  - 多个中间件会形成一个栈结构，以先进后出的顺序执行
  - 最外层的中间件首先执行
  - 调用next函数，将执行权交给下一个中间件
  - 最内层的中间件最后执行
  - 执行结束后，把执行权交回上一层

  ```javascript
  const koa = require('koa')
  
  const app = new koa()
  
  const one = (ctx,next) => {
      console.log('1')
      next()
      console.log('one')
  }
  
  const two = (ctx,next) => {
      console.log('2')
      next()
      console.log('two')
  }
  
  const three = (ctx,next) => {
      console.log('3')
      next()
      console.log('three')
  }
  
  app.use(one)
  app.use(two)
  app.use(three)
  
  app.listen(3001,() => {
      console.log('koa....')
  })
  ```

  这段代码就是按照 ` 1 2 3 three two one`的顺序打印的，根据注册中间件的顺序，以洋葱模型先入后出。one先入栈，执行到next时开始执行下一个中间件，到最后才会回到one。

- 异常捕获

  因为洋葱模型使得koa错误捕获非常方便，只需要在第一个中间件中对错误进行捕获即可。

  ```javascript
  app.use(async (ctx,next) =>{
  	try{
  		await next()
  	}cartch(err) {
  		ctx.status = 500
  		ctx.body = '服务器内部错误'
  	}
  })
  ```

##### 原理实现