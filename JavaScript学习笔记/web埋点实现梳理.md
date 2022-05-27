











前端监控系统搭建

当用户在使用产品时遇到JavaScript报错，没有开发背景的都会意识到页面卡顿了，JavaScript报错都会阻塞后续流程，如果报错的地方比较靠前，有些页面数据没有拿到，页面甚至都会出现白屏状况，这种生产bug在给到开发人员时，也只会在测试环境复现这个bug，通过控制台来查看调用栈和报错信息。如果这个bug不太好复现，开发人员解决的难度就会大很多，这个时候如果bug发生时的即时报错信息、函数调用栈，修复bug的难度和时间成本就会大大降低。

这只是说的其中异常监控一个方面，一个优秀的完善的前端监控系统不仅仅是异常监控，还囊括性能监控、数据埋点，行为采集等，他能做的事情和前景还是很多的。接下来就按照异常监控、性能监控、数据埋点、行为采集这四个方面来介绍。

##### 异常监控

异常监控包括JavaScript语法错误，资源加载错误，接口异常，我们挨个来介绍。

首先熟悉一个事件，[GlobalEventHandlers.onerror](https://developer.mozilla.org/zh-CN/docs/Web/API/GlobalEventHandlers/onerror)，详细可以查看MDN。

- 当JavaScript语法运行错误时，window会触发一个ErrorEvent接口的error事件，并执行window.onerror()。
- 当资源加载失败，加载资源的元素会触发与一个Event接口的error事件，并执行该元素上的onerror()处理函数，这些事件不会冒泡到window，会被单一的window.addEventlistener捕获。





##### 性能监控





##### 数据埋点





##### 行为采集















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



