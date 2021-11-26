#####  XMLHttpRequest对象

所有现代浏览器都通过 XMLHttpRequest 构造函数原生支持 XHR 对象：

```
let xhr = new XMLHttpRequest()

xhr.open("get", "example.php", false);
xhr.send(null); 
```

 第二行代码就可以向 `example.php` 发送一个同步的 GET 请求。关于这行代码需要说明几点。首先，这 里的 URL 是相对于代码所在页面的，当然也可以使用绝对 URL。其次，调用 open()不会实际发送请 求，只是为发送请求做好准备。 

send()方法接收一个参数，是作为请求体发送的数据。如果不需要发送请求体，则必须传 null， 因为这个参数在某些浏览器中是必需的。调用 send()之后，请求就会发送到服务器。

因为这个请求是同步的，所以 JavaScript 代码会等待服务器响应之后再继续执行。收到响应后，XHR 对象的以下属性会被填充上数据：

- [ ]  responseText：作为响应体返回的文本。  
- [ ]  responseXML：如果响应的内容类型是"text/xml"或"application/xml"，那就是包含响应 数据的 XML DOM 文档。  
- [ ]  status：响应的 HTTP 状态。
- [ ]  statusText： 响应的 HTTP 状态描述 

 收到响应后，第一步要检查 status 属性以确保响应成功返回。 

```
if ((xhr.status >= 200 && xhr.status < 300) || xhr.status == 304) {
 alert(xhr.responseText);
} else {
 alert("Request was unsuccessful: " + xhr.status);
} 
```

 XHR 对象有一个 readyState 属性，表示当前处在请求/响应过程的哪个阶段。 

- [ ] 0： 未初始化（Uninitialized）。尚未调用 open()方法 
- [ ] 1： 已打开（Open）。已调用 open()方法，尚未调用 send()方法。 
- [ ] 2： 已发送（Sent）。已调用 send()方法，尚未收到响应。 
- [ ] 3： 接收中（Receiving）。已经收到部分响应 
- [ ] 4： 完成（Complete）。已经收到所有响应，可以使用了。 

每次 readyState 从一个值变成另一个值，都会触发 readystatechange 事件。可以借此机会检 查 readyState 的值。一般来说，我们唯一关心的 readyState 值是 4，表示数据已就绪。为 



##### fetch

Fetch API 能够执行 XMLHttpRequest 对象的所有任务，但更容易使用，接口也更现代化，能够在 Web 工作线程等现代 Web 工具中使用。XMLHttpRequest 可以选择异步，而 Fetch API 则必须是异步。

Fetch API 本身是使用 JavaScript 请求资源的优秀工具，同时这个 API 也能够应用在服务线程 （service worker）中，提供拦截、重定向和修改通过 fetch()生成的请求接口。 

 fetch()方法是暴露在全局作用域中的，包括主页面执行线程、模块和工作线程。调用这个方法， 浏览器就会向给定 URL 发送请求。 

```javascript
fetch('http://example.com/movies.json')
  .then(response => response.json())
  .then(data => console.log(data));
```

这里我们通过网络获取一个 JSON 文件并将其打印到控制台。最简单的用法是只提供一个参数用来指明想 `fetch()` 到的资源路径，然后返回一个包含响应结果的 promise 。

Fetch API 支持通过 Response 的 status（状态码）和 statusText（状态文本）属性检查响应状 态。成功获取响应的请求通常会产生值为 200 的状态码 ：

```javascript
fetch('/bar')
 .then((response) => {
 console.log(response.status); // 200
 console.log(response.statusText); // OK
 }); 
```



只使用 URL 时，fetch()会发送 GET 请求，只包含最低限度的请求头。要进一步配置如何发送请 求，需要传入可选的第二个参数 init 对象：

- [ ] body，指定使用请求体时请求体的内容，必须是 Blob、BufferSource、FormData、URLSearchParams、ReadableStream 或 String 的 实例 
- [ ]  cache ， 用于控制浏览器与 HTTP缓存的交互。要跟踪缓存的重定向，请求的 redirect 属性值必须是"follow"， 而且必须符合同源策略限制。 
- [ ]  method ， 指定 HTTP 请求方法 
- [ ]  headers ， 用于指定请求头部 

```javascript
let payload = JSON.stringify({
 foo: 'bar'
});
let jsonHeaders = new Headers({
 'Content-Type': 'application/json'
});
fetch('/send-me-json', {
 method: 'POST', // 发送请求体时必须使用一种 HTTP 方法
 body: payload,
 headers: jsonHeaders
});
```

Fetch 也支持通过 AbortController/AbortSignal 对中断请求。调用 AbortController. abort()会中断所有网络传输，特别适合希望停止传输大型负载的情况。中断进行中的 fetch()请求会 导致包含错误的拒绝：

```
let abortController = new AbortController();
fetch('wikipedia.zip', { signal: abortController.signal })
 .catch(() => console.log('aborted!');
// 10 毫秒后中断请求
setTimeout(() => abortController.abort(), 10);
// 已经中断 
```



同样也可以使用自定义请求对象， 除了传给 `fetch()` 一个资源的地址，你还可以通过使用 [`Request()`](https://developer.mozilla.org/zh-CN/docs/Web/API/Request/Request) 构造函数来创建一个 request 对象，然后再作为参数传给 `fetch()`： 

```javascript
const myHeaders = new Headers();

const myRequest = new Request('flowers.jpg', {
  method: 'GET',
  headers: myHeaders,
  mode: 'cors',
  cache: 'default',
});

fetch(myRequest)
  .then(response => response.blob())
  .then(myBlob => {
    myImage.src = URL.createObjectURL(myBlob);
  });
```

 使用 `Headers` 的接口，你可以通过 `Headers()`构造函数来创建一个你自己的 headers 对象。 

```javascript
const myHeaders = new Headers({
  'Content-Type': 'text/plain',
  'Content-Length': content.length.toString(),
  'X-Custom-Header': 'ProcessThisImmediately'
});
```

使用`response`的接口，可以通过`response`构造函数来创建一个自定义的`response`

```javascript
let r = new Response('foobar', {
 status: 418,
 statusText: 'I\'m a teapot'
});
console.log(r); 
```



fetch相比xhr优点：

- 符合关注分离，没有将输入、输出和用事件来跟踪的状态混杂在一个对象里
- 更加底层，提供的API丰富（request, response）
- 脱离了XHR，是ES规范里新的实现方式
- fetchtch只对网络请求报错，对400，500都当做成功的请求，需要封装去处理
- fetch默认不会带cookie，需要添加配置项
- fetch不支持abort，不支持超时控制，使用setTimeout及Promise.reject的实现的超时控制并不能阻止请求过程继续在后台运行，造成了量的浪费
- fetch没有办法原生监测请求的进度，而XHR可以。