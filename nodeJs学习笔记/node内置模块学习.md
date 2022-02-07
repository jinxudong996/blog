

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
- writeFile：向指定文件中写入数据
- appendFile：追加的方式向执行文件中写入数据
- copyFile：将某个文件中的数据拷贝至另一个文件
- watchFile：对指定文件进行监控

