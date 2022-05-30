











前端监控系统搭建

当用户在使用产品时遇到JavaScript报错，没有开发背景的都会意识到页面卡顿了，JavaScript报错都会阻塞后续流程，如果报错的地方比较靠前，有些页面数据没有拿到，页面甚至都会出现白屏状况，这种生产bug在给到开发人员时，也只会在测试环境复现这个bug，通过控制台来查看调用栈和报错信息。如果这个bug不太好复现，开发人员解决的难度就会大很多，这个时候如果bug发生时的即时报错信息、函数调用栈，修复bug的难度和时间成本就会大大降低。

这只是说的其中异常监控一个方面，一个优秀的完善的前端监控系统不仅仅是异常监控，还囊括性能监控、数据埋点，行为采集等，他能做的事情和前景还是很多的。接下来就按照异常监控、性能监控、数据埋点、行为采集这四个方面来介绍。

##### 异常监控

异常监控包括JavaScript语法错误，资源加载错误，**接口异常**，我们挨个来介绍。

所有的错误可以归类为以下七种：

- SyntaxError 语法错误，是代码解析时发生的错误，比如：

  ```javascript
  let a = 
  //"Uncaught SyntaxError: Unexpected end of input"
  ```

- TypeError 类型错误，是变量或者参数不是预期类型时发生的错误，比如

  ```javascript
  let a = 12;
  a.concat(9)
  ```

- RangeError 范围错误是一个值超出范围是发生的错误，比如设置数组长度为负值

  ```javascript
  new Array(-1)
  ```

- ReferenceError  引用错误，是引用一个不存在的变量时发生的错误

  ```javascript
  console.log(a)
  ```

- EvalError eval错误，是eval函数没有被正确执行时抛出的错误，不过现在这个错误已经不再使用了，通常都会抛出TypeError 类型

  ```javascript
  eval = () => {}
  new eval()
  ```

- RUIError URI错误，是在调用decodeRUI、encodeURI、decodeURIComponent这类浏览器提供方法时发生的错误

  ```javascript
  decodeURIComponent('%')
  ```

- Failed to load resource 资源加载错误，是指img、input等标签加载资源时报错了

上述错误都可以被一个事件对象所监控，[GlobalEventHandlers.onerror](https://developer.mozilla.org/zh-CN/docs/Web/API/GlobalEventHandlers/onerror)，详细可以查看MDN。

- 当JavaScript语法运行错误时，window会触发一个ErrorEvent接口的error事件，并执行window.onerror()。
- 当资源加载失败，加载资源的元素会触发与一个Event接口的error事件，并执行该元素上的onerror()处理函数，这些事件不会冒泡到window，会被单一的window.addEventlistener捕获。

```javascript
//js语法错误
window.onerror = (msg, url, line, column, error,a,b) => {
  reportData({
      msg,
      line,
      column,
      error: error.stack,
      subType: 'js',
      pageURL: url,
      type: 'error',
      startTime: performance.now(),
  })
}
```

```javascript
//资源加载错误
window.addEventListener('error', e => {
  const target = e.target
  if (!target) return

  if (target.src || target.href) {
      const url = target.src || target.href
      reportData({
          url,
          type: 'error',
          subType: 'resource',
          startTime: e.timeStamp,
          html: target.outerHTML,
          resourceType: target.tagName,
          paths: e.path.map(item => item.tagName).filter(Boolean),
      })
  }
}, true)
```

目前上报数据就暂时先打印出来：

```javascript
function reportData(options){
  console.log(options)
}
```

接下来测试一下：

```
//js语法报错
column: 15
error: "ReferenceError: a is not defined\n    at file:///C:/Users/Thomas%E4%B8%9C/Desktop/owl/index.html:12:15"
line: 12
msg: "Uncaught ReferenceError: a is not defined"
pageURL: "file:///C:/Users/Thomas%E4%B8%9C/Desktop/owl/index.html"
startTime: 42.5
subType: "js"
type: "error"

//资源加载报错
html: "<img src=\"a.png\" alt=\"\">"
paths: (3) ['IMG', 'BODY', 'HTML']
resourceType: "IMG"
startTime: 45
subType: "resource"
type: "error"
url: "file:///C:/Users/Thomas%E4%B8%9C/Desktop/owl/a.png"
```



##### 性能监控

性能监控一半都通过浏览器的performance对象来获取常规的新能指标，关于performance可以从[MDN](https://developer.mozilla.org/zh-CN/docs/Web/API/Performance)来简单的了解一下这个对象：

>  **`Performance`** 接口可以获取到当前页面中与性能相关的信息。它是 High Resolution Time API 的一部分，同时也融合了 Performance Timeline API、[Navigation Timing API](https://developer.mozilla.org/en-US/docs/Web/API/Navigation_timing_API)、 [User Timing API](https://developer.mozilla.org/en-US/docs/Web/API/User_Timing_API) 和 [Resource Timing API](https://developer.mozilla.org/en-US/docs/Web/API/Resource_Timing_API)。 

这个

这个对象上有着很多的属性和方法，接下来列举一些常用的值：

- navigation  这个对象表示出现在当前浏览上下文的 navigation 类型，比如获取某个资源所需要的重定向次数。 

- timimg  这个对象包括了页面相关的性能信息。这个对象上有很多需要关注的属性，接下来一一介绍下：

  - navigationStart 浏览器处理当前网页的启动时间
  -  fetchStart  浏览器发起http请求读取文档的毫秒时间戳
  -  domainLookupStart  域名查询开始的时间戳
  -  domainLookupEnd    域名查询结束的时间戳
  -  connectStart   http请求开始向服务器发送的时间戳
  -  connectEnd  浏览器与服务器建立连接（握手和认证过程结束）的毫秒时间戳
  -  requestStart  浏览器向服务器发出http请求的时间戳，或者是开始读取本地缓存的时间戳
  -   responseStart  浏览器从服务器（或者读取本地缓存）收到第一个字节的时间戳
  -  responseEnd  浏览器从服务器收到最后一个字节的时间戳
  -  domLoading   浏览器开始解析网页DOM结构的时间
  -  domInteractive  网页DOM树创建完成，开始加载内嵌资源的时间
  -  domContentLoadedEventEnd   网页所有需要执行的脚本执行完成的时间，domReady的时间
  -  domContentLoadedEventStart  网页domContentLoaded事件发生时的时间戳
  -  domComplete   网页dom结构生成的时间戳
  -  loadEventEnd  网页load事件的回调函数执行的时间戳
  -  loadEventStart   网页load事件的回调函数结束运行的时间戳

  根据上面一些属性，可以获得一些有趣的性能指标：

  ![](C:\Users\Thomas东\Desktop\owl\index.png)

​    其中：

- DNS查询耗时可以对开发者的CDN服务器工作是否正常做出反馈
- 请求响应耗时能对返回模板中同步数据的情况做出反馈
- 有DOM解析耗时可以观察出我们的DOM结构是否合理，以及是否有JavaScript阻塞我们页面解析
- 内容传输耗时可以检测出我们网络通路是否正常，大多数情况下新能问题是网络或者运行商本身问题
- 资源加载耗时一般情况下是文档的下载时间，主要是观察以下文档流体积是否过大
- DOM_READY耗时通常是DOM树解析完成后，网页内资源加载完成时间，比如JavaScript脚本加载执行完成，这个阶段一般情况下可能会触发domContentLoaded事件。
- 首次渲染耗时表述的是浏览器去加载文档到用户能够看到第一帧非空图像的时间，也叫白屏时间
- 首次可交互耗时的是DOM树解析完成的时间，本阶段Document.readyState的状态值为interactive，并且会抛出readyStateChange事件
- 首包时间耗时是浏览器对文档发起查找DNS的请求，到请求返回给浏览器第一个字节数据的时间，这个时间反馈的是DNS域名解析查找的时间
- 页面完全加载耗时指的是下载整个页面的总时间，一般情况下指浏览器对一个URL发起请求到把这个URL上所需要的文档下载下来的时间，这个数据主要受网络环境文档大小的影响
- SSL连接耗时反馈的是数据安全性，完整性建立耗时
- TCP连接耗时指的是建立起连接过程的耗时，TCP协议主要工作与传输层，是一种比UDP更为安全的传输协议



##### 行为采集

这里打算采集一些除了性能之外的一些有价值的数据。



###### 环境相关数据

我们在追查问题时，除了报错信息，知道问题出在那种设备上、操作的用户、用户权限客户端版本等，这些数据都能够很好的帮助我们更加深入的了解bug发生的原因。这些数据我们打算让他当做公共数据，也就是每一条上报的数据都会携带的，它包含这样几个：

- pid，接入产品标识
- uid，用户id
- version  当前项目的版本
- ua，userAgent，浏览器默认获取相关IP、型号、操作系统等

###### 平均在线时长

用户平均在线也是一个很有价值的





##### 数据埋点





##### 















##### 性能指标

chrome提出了一个以用户为中心的性能指标，以用户为中心的性能指标是了解和改善您的网站体验的一大重要工具，这些指标将使真实用户受益。 详细查看[文档](https://web.dev/metrics/)

###### FP

 FP(first-paint)，从页面加载开始到第一个像素绘制到屏幕上的时间，实际上也可以理解为白屏时间。

```javascript
const entryHandler = (list) => {        
    for (const entry of list.getEntries()) {
        if (entry.name === 'first-paint') {
            observer.disconnect()
        }

       console.log(entry)
    }
}

const observer = new PerformanceObserver(entryHandler)
// buffered 属性表示是否观察缓存数据，也就是说观察代码添加时机比事情触发时机晚也没关系。
observer.observe({ type: 'paint', buffered: true })
```

打印的数据中心的startTime就是我们要的绘制白屏时间。

###### FCP

FCP(first-contentful-paint)，从页面加载开始到页面内容的任何部分在屏幕上完成渲染的时间 

```javascript
const entryHandler = (list) => {        
    for (const entry of list.getEntries()) {
        if (entry.name === 'first-contentful-paint') {
            observer.disconnect()
        }
        
        console.log(entry)
    }
}

const observer = new PerformanceObserver(entryHandler)
observer.observe({ type: 'paint', buffered: true })
```

###### LCP

LCP(largest-contentful-paint)，从页面加载开始到最大文本块或图像元素在屏幕上完成渲染的时间。LCP 指标会根据页面[首次开始加载](https://w3c.github.io/hr-time/#timeorigin-attribute)的时间点来报告可视区域内可见的最大[图像或文本块](https://web.dev/lcp/#what-elements-are-considered)完成渲染的相对时间。 

```javascript
const entryHandler = (list) => {
    if (observer) {
        observer.disconnect()
    }

    for (const entry of list.getEntries()) {
        console.log(entry)
    }
}

const observer = new PerformanceObserver(entryHandler)
observer.observe({ type: 'largest-contentful-paint', buffered: true })
```

FCP 和 LCP 的区别是：FCP 只要任意内容绘制完成就触发，LCP 是最大内容渲染完成时触发。 

###### CLS

CLS(layout-shift)，从页面加载开始和其[生命周期状态](https://developers.google.com/web/updates/2018/07/page-lifecycle-api)变为隐藏期间发生的所有意外布局偏移的累积分数。 



###### 首屏渲染时间

大多数的情况下，首屏渲染时间可以通过load事件来获取，当纯HTML被完全加载以及解析时，DOMContentLoaded事件会被触发，不用去等待css、img、iframe加载完。当整个页面及其所有的依赖被加载完时，将会触发load事件。







###### TTFB

首字节时间 (TTFB) 是衡量实验室和现场连接设置时间和 Web 服务器响应能力的基本指标。它有助于识别 Web 服务器何时响应请求太慢。在导航请求（即对 HTML 文档的请求）的情况下，它优先于所有其他有意义的加载性能指标 



###### FCP



###### LCP



###### FID



###### TTI



###### TBT



###### CLS



###### INP



