##### 模块化

- 模块导入导出

  新建`main.js`文件，写入代码

  ```javascript
  const age = 18
  const addFn = (x,y) => {
      return x+y
  }
  
  module.exports = {
      age,
      addFn
  }
  ```

  在`index.js`中进行导入：

  ```javascript
  let obj = require('./main.js')
  
  console.log(obj)
  ```

  

- module属性及其常见信息获取

  module的属性上记录了该模块导出的内容、引用信息等

  ```
   Module {
    id: 'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node\\commonJs\\main.js',
    path: 'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node\\commonJs',       
    exports: { age: 18, addFn: [Function: addFn] },
    parent: Module {
      id: '.',
      path: 'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node\\commonJs',
      exports: {},
      parent: null,
      filename: 'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node\\commonJs\\index.js',
      loaded: false,
      children: [ [Circular *1] ],
      paths: [
        'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node\\commonJs\\node_modules',
        'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node\\node_modules',
        'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node_modules',
        'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\node_modules',
        'C:\\Users\\Thomas东\\Desktop\\blog\\node_modules',
        'C:\\Users\\Thomas东\\Desktop\\node_modules',
        'C:\\Users\\Thomas东\\node_modules',
        'C:\\Users\\node_modules',
        'C:\\node_modules'
      ]
    },
    filename: 'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node\\commonJs\\main.js',
    loaded: false,
    children: [],
    paths: [
      'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node\\commonJs\\node_modules',
      'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node\\node_modules',
      'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\code\\node_modules',
      'C:\\Users\\Thomas东\\Desktop\\blog\\webpack学习\\node_modules',
      'C:\\Users\\Thomas东\\Desktop\\blog\\node_modules',
      'C:\\Users\\Thomas东\\Desktop\\node_modules',
      'C:\\Users\\Thomas东\\node_modules',
      'C:\\Users\\node_modules',
      'C:\\node_modules'
    ]
  }
  ```

  

- exports导出数据

  可以直接给exports对象添加属性来导出数据

  ```
  exports.name = 'nick'
  ```

- 模拟require的实现

  模拟require主要有两个步骤，首先解析所传入的路径，随后根据路径找到文件内容执行即可。在执行之前，首先放到缓存对象中，查找时先查找缓存对象，即缓存优先。

  ```javascript
  const { dir } = require('console')
  const fs = require('fs')
  const path = require('path')
  const vm = require('vm')
  
  function Module (id) {
    this.id = id
    this.exports = {}
    console.log(1111)
  }
  
  Module._resolveFilename = function (filename) {
    // 利用 Path 将 filename 转为绝对路径
    let absPath = path.resolve(__dirname, filename)
    
    // 判断当前路径对应的内容是否存在（）
    if (fs.existsSync(absPath)) {
      // 如果条件成立则说明 absPath 对应的内容是存在的
      return absPath
    } else {
      // 文件定位
      let suffix = Object.keys(Module._extensions)
  
      for(var i=0; i<suffix.length; i++) {
        let newPath = absPath + suffix[i]
        if (fs.existsSync(newPath)) {
          return newPath
        }
      }
    }
    throw new Error(`${filename} is not exists`)
  }
  
  Module._extensions = {
    '.js'(module) {
      // 读取
      let content = fs.readFileSync(module.id, 'utf-8')
  
      // 包装
      content = Module.wrapper[0] + content + Module.wrapper[1] 
      
      // VM 
      let compileFn = vm.runInThisContext(content)
  
      // 准备参数的值
      let exports = module.exports
      let dirname = path.dirname(module.id)
      let filename = module.id
  
      // 调用
      compileFn.call(exports, exports, myRequire, module, filename, dirname)
    },
    '.json'(module) {
      let content = JSON.parse(fs.readFileSync(module.id, 'utf-8'))
  
      module.exports = content
    }
  }
  
  Module.wrapper = [
    "(function (exports, require, module, __filename, __dirname) {",
    "})"
  ]
  
  Module._cache = {}
  
  Module.prototype.load = function () {
    let extname = path.extname(this.id)
    
    Module._extensions[extname](this)
  }
  
  function myRequire (filename) {
    // 1 绝对路径
    let mPath = Module._resolveFilename(filename)
    
    // 2 缓存优先
    let cacheModule = Module._cache[mPath]
    if (cacheModule) return cacheModule.exports
  
    // 3 创建空对象加载目标模块
    let module = new Module(mPath)
  
    // 4 缓存已加载过的模块
    Module._cache[mPath] = module
  
    // 5 执行加载（编译执行）
    module.load()
  
    // 6 返回数据
    return module.exports
  }
  ```

  

##### 事件

nodeJs中事件都是以发布订阅模式，使用on订阅事件，使用emit来发布。

```javascript
const EventEmitter = require('events')

const ev = new EventEmitter()

ev.on('事件1',() => {
    console.log('事件1执行')
})

ev.emit('事件1')
```

##### 通信

- 网络层次模型

  为了方便网络维护管理实施，一共推出了两种网络层次模型：OSI七层模型和TCP/IP四层模型

  OSI七层模型：

  - 应用层：用户与网络的接口，有这个各种面向具体应用的协议，比如HTTP、FTP、SSH等
  - 表示层：数据加密、转换、压缩
  - 会话层：控制网络连接建立与终止
  - 传输层：控制数据传输可靠性，相当于TCP/IP里的传输层
  - 网络层：确定目标网络，相当于TCP/IP里的网际层
  - 数据链路层：确定目标主机
  - 物理层：各种物理设备和标准

  TCP/IP就是在此基础上将引用层、表示层、会话层合并为引用层，最下面的数据链路层和物理层合并为连接层。

- TCP协议

  TCP属于传输层协议，是面向连接的，用于处理实时通信。

  常见的控制字段有：SYN=1表示请求建立连接、FIN=1表示请求断开连接、ACK=1表示数据信息确认

  TCP三次握手与四次挥手：

  ![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b21895dd30f8492797b11c2d38fe0534~tplv-k3u1fbpfcp-watermark.awebp)

  首先三次握手建立连接，客户端向服务端发送SYN=1表示请求链接，服务端发送ACK=1表示信息确认，这里只是建立了一条由客户端向服务端发送信息的通道，还需要建立服务端向客户端的通道。服务端向客户端发送SYN=1表示请求链接，客户端向服务端发送ACK=1表示信息确认，这里一共有这四次握手，只不过第二次和第三次可以合并在一起，即三次握手。

  四次挥手和三次握手的过程类似，即客户端向服务端发送FIN=1表示断开连接，服务端发送ACK=1表示信息确认，服务端向客户端发送FIN=1表示断开连接，客户端发送ACK=1表示信息确认。这里四次挥手为何第二次第三次不合并发送呢，因为当服务端收到客户端的SYN连接请求报文后，可以直接发送SYN+ACK报文。其中ACK报文是用来应答的，SYN报文是用来同步的。但是关闭连接时，当服务端收到FIN报文时，很可能并不会立即关闭SOCKET，所以只能先回复一个ACK报文，告诉客户端，"你发的FIN报文我收到了"。只有等到我服务端所有的报文都发送完了，我才能发送FIN报文，因此不能一起发送。故需要四次挥手。