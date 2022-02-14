express学习笔记

##### 起步

给予nodeJs平台，快速、开放、极简的web开发框架

```javascript
const express = require('express')

const app = express()

app.get('/',(req,res) => {
    res.send('hello,world')
})

app.listen(3000,() => {
    console.log('server start---')
})
```

上面代码便创建了一个简易的web服务器，访问`http://localhost:3000/`便可看到hello，world。

##### 路由基础

路由是指确定应用程序如何响应客户端对特定端点的请求，该端点是URI和特定的HTTP请求方法（GET、POST等）。每个路由可以具有一个或多个处理程序函数，这个函数在匹配改路由时执行。

比如：

```javascript
app.get('/',(req,res) => {
    res.send('hello,world')
})
```

##### 中间件

中间件和AOP面向切面编程就是一个意思，都需要经过一些步骤，不去修改自己的代码，以此来扩展或者处理一些功能。

比如这个每次响应前打印日志的函数，就是中间件

```javascript
const express = require('express')

const app = express()

app.use((req,res,next) => {
    console.log(req.method,req.url,Date.now())
    next()
})

app.get('/',(req,res) => {
    res.send('hello,world')
})

app.get('/about',(req,res) => {
    res.send('hello,about')
})
app.listen(3000,() => {
    console.log('server start---')
})
```

express中应用程序可以使用以下类型的中间件：

- 应用程序级别中间件

  - 不做任何限定的中间件，所有的路由都会匹配进来

  ```javascript
  app.use((req,res,next) => {
      console.log(req.method,req.url,Date.now())
      next()
  })
  ```

  - 限定请求路径

    ```javascript
    app.use('/about',(req,res,next) => {
        console.log(req.method,req.url,Date.now())
        next()
    })
    ```

  - 指定多个中间件

    ```javascript
    app.use('/about',(req,res,next) => {
        console.log(req.method,req.url,Date.now())
        next()
    })
    app.use('/about',(req,res,next) => {
        console.log(req.method,req.url,Date.now())
        next()
    })
    ```

    

- 路由级别中间件

  可以将路由封装成一个模块，以中间件的形式来挂在路由

  ```javascript
  //mr.js
  const express = require('express')
  
  const router = express.Router()
  
  router.get('/foo',(req,res) => {
      res.send('foo')
  })
  
  module.exports =  router
  ```

  ```javascript
  const MRrouter = require('./mr.js')
  
  const app = express()
  
  app.use(MRrouter)
  ```

  

- 错误处理中间件

  在服务的最后捕获错误

  ```javascript
  app.use((err,req,res,next) => {
      console.log('错误')
      res.status(500).json({
          error:err.message
      })
  })
  ```

  这里需要在路由是捕获错误，并且将错误信息传给next()

- 内置中间件

  express本身提供了以下五个中间件

  - express,json() 解析Content-Type为application/json格式的请求体
  - express.urlencoded()解析Content-Type为application/x-www-form-urlencoded格式的请求体
  - express.raw()解析Content-Type为application/octet-stream格式的请求体
  - express.text()解析Content-Type为text/plain格式的请求体
  - express.static()托管静态资源

##### 原理实现

接下来实现一个简易的express

```javascript
//app.js
const express = require('./express')

const app = express()

app.get('/',(req,res) => {
    res.end('get /')
})

app.get('/foo',(req,res) => {
    res.end('get /foo')
})

app.listen(3001, () => {
    console.log('listen at 3001')
})
```

新建`express/index.js`

```javascript
module.exports = require('./lib/express')
```

新建`express/lib/express.js`

```javascript
const http = require('http')
const url = require('url')
const routes = []

function createApplication() {
    return {
        get(path,handler) {
            routes.push({
                path,
                method:'get',
                handler
            })
        },
        listen(...args) {
            const server = http.createServer((req,res) => {
                const {pathname} = url.parse(req.url)
                const method = req.method.toLowerCase()
                const route = routes.find(route => route.path === pathname && route.method === method)
                if(route){
                    return route.handler(req,res)
                }
                res.end('404')
            })
            server.listen(...args)
        }
    }
}

module.exports = createApplication
```

启动`node app.js`即可实现简易的路由功能

然而这种方式直接在createApplication中返回一个对象，扩展性很差，可以添加一个application模块，将对应的方法添加到对象上：

新建`application.js`

```javascript
const http = require('http')
const url = require('url')
const routes = []

function App(){}

App.prototype.get = function (path,handler) {
    routes.push({
        path,
        method:'get',
        handler
    })
},

App.prototype.listen = function(...args) {
    const server = http.createServer((req,res) => {
        const {pathname} = url.parse(req.url)
        const method = req.method.toLowerCase()
        const route = routes.find(route => route.path === pathname && route.method === method)
        if(route){
            return route.handler(req,res)
        }
        res.end('404')
    })
    server.listen(...args)
}

module.exports = App
```

```javascript
//express.js
const App = require("./application")

function createApplication() {
   return new App()
}

module.exports = createApplication
```

运行`node  app.js`即可

