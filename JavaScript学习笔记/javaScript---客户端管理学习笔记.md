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
- [ ] 域，cookie有效的域，发送到这个域的所有的请求都会包含对应的cookie，这个值



















#### 浏览器存储API

































#### IndexedBD



