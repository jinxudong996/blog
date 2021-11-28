#### cookie

HTTP cookie 通常也叫作 cookie，最初用于在客户端存储会话信息。这个规范要求服务器在响应 HTTP 请求时，通过发送 Set-Cookie HTTP 头部包含会话信息。 

```
HTTP/1.1 200 OK
Content-type: text/html
Set-Cookie: name=value
Other-header: other-header-value
```

这个 HTTP 响应会设置一个名为"name"，值为"value"的 cookie。名和值在发送时都会经过 URL 编码。浏览器会存储这些会话信息，并在之后的每个请求中都会通过 HTTP 头部 cookie 再将它们发回服 务器。

##### 限制

cookie 是与特定域绑定的。设置 cookie 后，它会与请求一起发送到创建它的域。这个限制能保证 cookie 中存储的信息只对被认可的接收者开放，不被其他域访问。 因为 cookie 存储在客户端机器上，所以为保证它不会被恶意利用，浏览器会施加限制。同时，cookie 也不会占用太多磁盘空间。 

- [ ] 不超过300个cookie
- [ ] 每个cookie不超过4096字节
- [ ] 每个域不超过20个cookie
- [ ] 每个域不超过81920字节

如果cookie总数超过了单个域的上限，会删除之前设置的cookie。如果创建的cookie超过了最大限制，则改cookie会被静默删除。



##### 构成

- [ ] 名称，唯一标识cookie的名称，且不区分大小写。
- [ ] 值，存储在cookie里的字符串值得经过URL编码
- [ ] 域，cookie有效的域，发送到这个域的所有的请求都会包含对应的cookie。
- [ ] 路劲，请求URL中包含这个路径才会把cookie发送到服务器
- [ ] 过期时间：表示何时删除cookie的时间戳
- [ ] 安全标志：设置之后，只会在SSL安全链接的情况下才会把cookie发送到服务器

```
Set-Cookie: name=value; expires=Mon, 22-Jan-07 07:10:24 GMT; domain=.wrox.com 
```

 这个头部设置一个名为"name"的 cookie，这个 cookie 在 2007 年 1 月 22 日 7:10:24 过期，对 www.wrox.com 及其他 wrox.com 的子域（如 p2p.wrox.com）有效 

`javascript`获取cookie比较简单，`document.cookie`返回页面中所有有效字段的cookie字符串，以分号分割。

​	

```
document.cookie
'_ga=GA1.2.350290494.1619427464; Hm_lvt_f89e0235da0841927341497d774e7b15=1637028239,1637316193,1637482021,1637831224; Hm_lpvt_f89e0235da0841927341497d774e7b15=1637831224; Hm_lvt_519d72adb78a0bf66de7bae18e994322=1637028243,1637030111,1637116399,1637843931; Hm_lpvt_519d72adb78a0bf66de7bae18e994322=1637908704'
```

阮一峰大佬的博客中返回的cookie，在控制台中输入` document.cookie = "name=Nicholas" `，然后打印cookie，既可以看见cookie后面加了个`name=Nicholas`

```
document.cookie
'_ga=GA1.2.350290494.1619427464; Hm_lvt_f89e0235da0841927341497d774e7b15=1637028239,1637316193,1637482021,1637831224; Hm_lpvt_f89e0235da0841927341497d774e7b15=1637831224; Hm_lvt_519d72adb78a0bf66de7bae18e994322=1637028243,1637030111,1637116399,1637843931; Hm_lpvt_519d72adb78a0bf66de7bae18e994322=1637908704; name=Nicholas'
```

`javaScript高级程序设计4`中封装了一个操作cookie方法：

```
class CookieUtil {
  static get(name) {
    let cookieName = `${encodeURIComponent(name)}=`,
    cookieStart = document.cookie.indexOf(cookieName),
    cookieValue = null;
    if (cookieStart > -1){
      let cookieEnd = document.cookie.indexOf(";", cookieStart);
      if (cookieEnd == -1){
        cookieEnd = document.cookie.length;
      }
      cookieValue = decodeURIComponent(document.cookie.substring(cookieStart+ cookieName.length, cookieEnd));
    }
    return cookieValue;
  }

  static set(name, value, expires, path, domain, secure) {
    let cookieText =
    `${encodeURIComponent(name)}=${encodeURIComponent(value)}`
    if (expires instanceof Date) {
      cookieText += `; expires=${expires.toGMTString()}`;
    }
    if (path) {
     cookieText += `; path=${path}`;
    }
    if (domain) {
      cookieText += `; domain=${domain}`;
    }
    if (secure) {
      cookieText += "; secure";
    }
     document.cookie = cookieText;
    }
  static unset(name, path, domain, secure) {
    CookieUtil.set(name, "", new Date(0), path, domain, secure);
  }
}; 
```

这个获取cookie的方法也就是通过字符串截取的操作。设置cookie也就常规，就是`document.cookie = cookieText;`，删除cookie的方法是设置一个空的cookie，过期时间 设置为1970 年 1 月 1 日，这样来删除cookie。 

##### 注意事项

还有一种叫作 HTTP-only 的 cookie。HTTP-only 可以在浏览器设置，也可以在服务器设置，但只能 在服务器上读取，这是因为 JavaScript 无法取得这种 cookie 的值。 因为所有 cookie 都会作为请求头部由浏览器发送给服务器，所以在 cookie 中保存大量信息可能会影 响特定域浏览器请求的性能。保存的 cookie 越大，请求完成的时间就越长。即使浏览器对 cookie 大小有 限制，最好还是尽可能只通过 cookie 保存必要信息，以避免性能问题。 



####  Web Storage  

>  Web Storage 最早是网页超文本应用技术工作组（WHATWG，Web Hypertext Application Technical Working Group）在 Web Applications 1.0 规范中提出的。这个规范中的草案最终成为了 HTML5 的一部分， 后来又独立成为自己的规范。Web Storage 的目的是解决通过客户端存储不需要频繁发送回服务器的数 据时使用 cookie 的问题 

>  Web Storage 的第 2 版定义了两个对象：localStorage 和 sessionStorage。localStorage 是 永久存储机制，sessionStorage 是跨会话的存储机制。这两种浏览器存储 API 提供了在浏览器中不 受页面刷新影响而存储数据的两种方式。2009 年之后所有主要供应商发布的浏览器版本在 window 对象 上支持 localStorage 和 sessionStorage。 

#####  Storage 

 Storage 类型用于保存名/值对数据，直至存储空间上限（由浏览器决定） 

 Storage 实例实现了以下方法：

- clear()，删除所有值，Firefox不兼容
- getItem(name)，取得给定的name值
- key(index)，取得给定数值位置的名称
- removeItem()，删除给定name的键值对
- setItem(name)，设置给定的name值



#####  sessionStorage 

>  sessionStorage 对象只存储会话数据，这意味着数据只会存储到浏览器关闭。这跟浏览器关闭时 会消失的会话 cookie 类似。存储在 sessionStorage 中的数据不受页面刷新影响，可以在浏览器崩溃 并重启后恢复。（取决于浏览器，Firefox 和 WebKit 支持，IE 不支持。）  

 sessionStorage 对象是 Storage 的实例，所以可以通过使用 setItem()方法或直接给属 性赋值给它添加数据。 

```
//方法写入
sessionStorage.setItem("name", "Nicholas"); 
//属性写入
sessionStorage.book = "Professional JavaScript";

// 使用方法取得数据
let name = sessionStorage.getItem("name");
// 使用属性取得数据
let book = sessionStorage.book; 
```

所有现代浏览器在实现存储写入时都使用了同步阻塞方式，因此数据会被立即提交到存储。具体 API 的实现可能不会立即把数据写入磁盘（而是使用某种不同的物理存储），但这个区别在 JavaScript 层 面是不可见的。通过 Web Storage 写入的任何数据都可以立即被读取。 

可以结合`sessionStorage` 的 length 属性和 key()方法遍历所有的值： 

```
for (let key in sessionStorage){
 let value = sessionStorage.getItem(key);
 alert(`${key}=${value}`);
}
```

 要从 sessionStorage 中删除数据，可以使用 delete 操作符直接删除对象属性，也可以使用 removeItem()方法 :

> ```
> // 使用 delete 删除值
> delete sessionStorage.name;
> // 使用方法删除值
> sessionStorage.removeItem("book");
> ```



#####  localStorage 

> 在修订的 HTML5 规范里，localStorage 对象取代了 globalStorage，作为在客户端持久存储 数据的机制。要访问同一个 localStorage 对象，页面必须来自同一个域（子域不可以）、在相同的端 口上使用相同的协议 

 localStorage 是 Storage 的实例 ,所以方法也基本一致。

```
// 使用方法存储数据
localStorage.setItem("name", "Nicholas");
// 使用属性存储数据
localStorage.book = "Professional JavaScript";
// 使用方法取得数据
let name = localStorage.getItem("name");
// 使用属性取得数据
let book = localStorage.book; 
```

 两种存储方法的区别在于，存储在 localStorage 中的数据会保留到通过 JavaScript 删除或者用户 清除浏览器缓存。localStorage 数据不受页面刷新影响，也不会因关闭窗口、标签页或重新启动浏览 器而丢失。 



##### 存储事件及限制

每当 Storage 对象发生变化时，都会在文档上触发 storage 事件。使用属性或 setItem()设置 值、使用 delete 或 removeItem()删除值，以及每次调用 clear()时都会触发这个事件。这个事件的 事件对象有如下 4 个属性：

- domain，存储变化对应的域
- key，被设置或者删除的键
- newValue，键被设置的新值，删除就是null
- oldValue，键变化之前的值

```
window.addEventListener("storage",
 (event) => console.log('Storage changed for ${event.domain}'));
```

 对于 sessionStorage 和 localStorage 上的任何更改都会触发 storage 事件，但 storage 事 件不会区分这两者。 

 不同浏览器给 localStorage 和 sessionStorage 设置了不同的空间限制，但大多数会限制为每个源 5MB 