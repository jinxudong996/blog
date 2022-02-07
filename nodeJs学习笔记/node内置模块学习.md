

#### path模块  

处理路径的模块

常用api：

##### basename()获取路径中的基础名称

```JavaScript
console.log(path.basename(__filename))
//index.js
```

返回路径中的最后一部分

##### diranme()获取路径中的目录名称

```
console.log(path.dirname(__filename))
//C:\Users\Thomas东\Desktop\blog\webpack学习\code\node\path  
```

返回路径中最后一个部分的上一层目录所在路径

##### extname()获取路径中扩展名称

```
console.log(path.extname(__filename))
//.js
```

返回路径的后缀

##### parse()解析路径

```javascript
const obj = path.parse('/a/b/c/index.js')
console.log(obj)
//
{
  root: '/',       
  dir: '/a/b/c',   
  base: 'index.js',
  ext: '.js',      
  name: 'index'    
}
```

##### isAbsolute()获取路径是否为绝对路径

```javascript
console.log(path.isAbsolute('foo'))
console.log(path.isAbsolute('/foo'))
//
false
true
```

##### join()拼接多个路径片段

```
console.log(path.join('a/b','c','index.js'))
//a\b\c\index.js
```

##### normalize()规范化路径

```
console.log(path.normalize('/a/b//c/index.html'))
//\a\b\c\index.html
```

##### resolve()返回绝对路径

```
console.log(path.resolve())
//C:\Users\Thomas东\Desktop\blog\webpack学习\code\node\path
```





#### buffer

一个全局变量，让js可以操作二进制。

##### 创建buffer实例

- alloc 创建指定字节大小的buffer

  ```javascript
  const b1 = Buffer.alloc(10)
  
  console.log(b1)
  //<Buffer 00 00 00 00 00 00 00 00 00 00>
  ```

  打印的b1就是10个字节的内存空间数据对象

- allocUnsafe 创建指定大小的buffer

  ```javascript
  const b2 = Buffer.allocUnsafe(10)
  
  console.log(b2)
  //<Buffer 18 42 f7 c4 49 01 00 00 08 00>
  ```

  这里的b2同样也是10个字节的内存空间，只不过这种创建方式不安全，allocUnsafe只要有空闲的空间就会被拿过来使用，可能会使用一些没有引用但依然有数据的空间。

- from 接受数据，创建buffer

  from接受数组、字符串和buffer对象来创建buffer

  ```javascript
  const b3 = Buffer.from('1')
  console.log(b3)
  //<Buffer 31>
  ```

  

##### buffer实例方法

- fill：使用数据填充buffer

  fill方法接受三个参数，第一个是填充的数据，第二第三个分别是填充的起始位置和结束位置，结束位置是取不到的

  ```javascript
  let buf = Buffer.alloc(6)
  
  buf.fill('123' , 0 ,3)
  console.log(buf)
  console.log(buf.toString())
  //
  <Buffer 31 32 33 00 00 00>
  123
  ```

  ```
  let buf = Buffer.alloc(6)
  
  buf.fill('123')
  console.log(buf)
  console.log(buf.toString())
  //
  <Buffer 31 32 33 31 32 33>
  123123
  ```

- write： 向buffer中写入数据

  同样也是接受三个参数，第一个填充的数据，第二个起始位置，第三个数据长度

  ```javascript
  buf.write('123',1,2)
  console.log(buf)
  console.log(buf.toString())
  //
  <Buffer 00 31 32 00 00 00>
  12
  ```

  ```javascript
  buf.write('123')
  console.log(buf)
  console.log(buf.toString())
  //
  <Buffer 31 32 33 00 00 00>
  123
  ```

  和fill不同的是，fill如果不指定位置，会重复数据直至填充满Buffer，而write只会填充所传入的数据

- toString： 从buffer中提取数据

- slice：  截取buffer

  接受两个参数，分别是起始位置和结束位置

  ```javascript
  buf.write('123456789')
  let b1 = buf.slice(3,5)
  console.log(b1)
  console.log(b1.toString())
  ```

  

- indexOf： 在buffer中查找数据

  用法同数组的indexOf一样，返回数据所在的索引，如果没有就返回-1

  ```JavaScript
  console.log(buf.indexOf('4'))
  //3
  ```

- copy：  拷贝buffer中的数据

  ```
  let b1 = Buffer.from('123')
  let b2 = Buffer.from('456')
  
  b2.copy(b1)
  
  console.log(b1.toString())
  console.log(b2.toString())
  //
  456
  456
  ```

#### 文件操作

##### 常见flag操作符

- r：表示可读
- w：表示可写
- s：表示同步
- +：表示执行相反操作
- x：表示排它操作
- a：表示追加操作

##### 文件操作API

- readFile：从指定文件中读取数据

  该函数接受三个参数。第一个是绝对路径，第二个编码格式，第三个回调函数

  ```javascript
  const fs = require('fs')
  const path = require('path')
  
  fs.readFile(path.resolve('data.txt'), 'utf-8', (err, data) => {
      console.log(err)
      console.log(data)
  })
  ```

  

- writeFile：向指定文件中写入数据

  重新覆盖该文件

  ```javascript
  fs.writeFile('data.txt', 'hello nodeJs', (err) => {
      if (!err) {
          fs.readFile(path.resolve('data.txt'), 'utf-8', (err, data) => {
              console.log(data)
          })
      }
  })
  ```

  

- appendFile：追加的方式向执行文件中写入数据

  ```javascript
  fs.appendFile('data.txt',' 追加成功',(err) => {
      console.log('追加成功~~')
  })
  ```

  

- copyFile：将某个文件中的数据拷贝至另一个文件

  ```javascript
  fs.copyFile('data.txt','text.txt',(err) => {
      console.log("copy success~~")
  })
  ```

  

- watchFile：对指定文件进行监控

  ```javascript
  fs.watchFile('data.txt',{interval:20},(curr,prev) => {
      if(curr.mtime !== prev.mtime){
          console.log('文件被修改了')
          fs.unwatchFile('data.txt')
      }
  })
  ```

  每20毫秒监听一次data.txt文件，一旦文件被修改，就打印随后取消监听

##### 大文件读写

上面的api都是一次性读文件的所有内容，一旦遇到较大文件就非常的慢，node也提供了open和close文件打开与关闭的操作。

- read

  读操作就是将数据从磁盘文件写入到buffer中，该方法接受五个参数，分别是fd定位当前被打开的文件，buf当前的缓冲区，offset当前从buf的那个位置开始执行写入，length表示当前写入的长度，position表示从当前文件的那个位置开始读取

  ```javascript
  const fs = require('fs')
  
  let buf = Buffer.alloc(10)
  
  fs.open('data.txt','r',(err,fd) => {
      console.log(fd)
      fs.read(fd,buf,0,4,0,(err,readBytes,data) => {
          console.log(readBytes)
          console.log(data)
          console.log(data.toString())
      })
  })
  // data.txt  内容是0123456789
  3
  4
  <Buffer 30 31 32 33 00 00 00 00 00 00>
  0123
  ```

  

- write

  将缓冲区的内容写入磁盘文件

  ```javascript
  let buf = Buffer.from('0123456789')
  
  fs.open('b.txt','w',(err,fd) => {
      fs.write(fd,buf,0,5,0,(err,writen,buffer) =>{
          console.log(writen)
          console.log(buffer)
          console.log(buffer.toString())
      })
  })
  //
  5
  <Buffer 30 31 32 33 34 35 36 37 38 39>
  0123456789
  ```

  

##### 实例：md文档抓换成html文件

思路：首先写一个html字符串当做模板，其中的样式使用`{{style}}`，内容使用`{{content}}`

来当占位符，分别读取md文件和css文件，来替换模板中的占位符。

代码：

```javascript
const fs = require('fs')
const path = require('path')
const {marked} = require('marked')
const browserSync = require('browser-sync')

let mdPath = path.join(__dirname, process.argv[2])
let cssPath = path.resolve('index.css')
let htmlPath = mdPath.replace(path.extname(mdPath), '.html')

fs.readFile(mdPath, 'utf-8', (err, data) => {
  // 将 md--》html
  let htmlStr = marked(data)
  console.log(htmlStr)
  fs.readFile(cssPath, 'utf-8', (err, data) => {
    let retHtml = temp.replace('{{content}}', htmlStr).replace('{{style}}', data)
    // 将上述的内容写入到指定的 html 文件中，用于在浏览器里进行展示
    fs.writeFile(htmlPath, retHtml, (err) => {
      console.log('html 生成成功了')
    })
  })
})

browserSync.init({
  browser: '',
  server: __dirname,
  watch: true,
  index: path.basename(htmlPath)
})

const temp = `
      <!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <title></title>
          <style>
              .markdown-body {
                  box-sizing: border-box;
                  min-width: 200px;
                  max-width: 1000px;
                  margin: 0 auto;
                  padding: 45px;
              }
              @media (max-width: 750px) {
                  .markdown-body {
                      padding: 15px;
                  }
              }
              {{style}}
          </style>
      </head>
      <body>
          <div class="markdown-body colorRed">
              {{content}}
          </div>
      </body>
      </html>
  `
```

