











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



用户平均在线也是一个很有价值的，这里是计算方法是：每次用户点击与下一次点击之间的时间做累加。每间隔5秒钟连续打点，超过15s就当做已经离线。这个后续还得继续优化。

```javascript
function averageOnlineTime (){
  //每5s打点
  //15分钟不点击  就认为离线
  let OFFLINE_MILL = 15*1000
  let SEND_MILL = 5*1000
  let lastTime = Date.now()

  window.addEventListener('click',() => {
    let now = Date.now()
    let duration = now - lastTime
    let onlineFlag = false

    if(duration > OFFLINE_MILL){
      //已经离线
      lastTime = Date.now()
      onlineFlag = true
      console.log('已经离线')
    }else if(duration > SEND_MILL){
      //5s连续打点
      lastTime = Date.now()

    }
    let durationData = {
      times:lastTime,
      flag:onlineFlag
    }
    reportData(durationData)
  },false)

}
```



###### 页面停留时间

 利用 addEventListener() 监听 popstate、hashchange 页面跳转事件。需要注意的是调用history.pushState()`或`history.replaceState()不会触发popstate事件。只有在做出浏览器动作时，才会触发该事件，如用户点击浏览器的回退按钮（或者在Javascript代码中调用history.back()或者history.forward()方法）。同理，hashchange也一样。



###### PV、PU

PV(page view) 是页面浏览量，UV(Unique visitor)用户访问量。PV 只要访问一次页面就算一次，UV 同一天内多次访问只算一次。

对于前端来说，只要每次进入页面上报一次 PV 就行，UV 的统计放在服务端来做，主要是分析上报的数据来统计得出 UV。



##### 数据上报

数据上报

常规的数据上报有三种方式：

- sendBeacon

  navigator.sendBeacon()可用于通过POST将少量数据异步传输到服务器。详细可见[MDN](https://developer.mozilla.org/zh-CN/docs/Web/API/Navigator/sendBeacon)。

  navigator.sendBeacon(url, data)，data参数就是要发送的数据，常见的类型有ArrayBuffer、ArrauBufferView、Blob、DomString、FormData等。

  这个方法主要用于满足统计和诊断代码的需要，兼容性较好（除了ie，主流的浏览器都支持），支持跨域，唯一缺点是支持传输的数据量较小。如何根据浏览器动态设置传输数据大小，这个得后续研究下他的最大数据值。

- XMLHttpRequest

  XMLHttpRequest（XHR）对象用于与服务器交互。通过 XMLHttpRequest 可以在不刷新页面的情况下请求特定 URL，获取数据。最常见的应用就是AJAX。然后这种方式他有一个弊端：当我们用ajax发送异步数据时，如果页面已经被卸载了，会导致发送失败的；如果我们用同步发送请求，他是会阻塞后续文档加载，有很大的性能问题，所以在页面卸载后发送请求，navigator.sendBeacon()相比XMLHttpRequest，前者是更好地选择。

- image

  image 方式是通过将采集的数据拼接在图片请求的后面，向服务端请求一个 1*1 px 大小的图片实现的，设置它的 src 属性就可以发送数据。这种方式简单且天然可跨域，又兼容所有浏览器，没有阻塞问题，是目前比较受欢迎的前端数据上报方式。但由于是 get 请求，对上报的数据量有一定的限制，一般为 2~8 kb。

  ```
  var img = new Image();
  img.width = 1;
  img.height = 1;
  img.src = '/sa.gif?project=default&data=xxx'
  ```

  但是这种方式也有一定的弊端，当关闭页面时，由于这种方式也是异步的，存在关闭页面时发送数据效果较差。

综上所述，数据上报采用sendBeacon方式，同时为兼容ie，需要判断如果是ie浏览器，就采用image方式上报。

##### 埋点





















