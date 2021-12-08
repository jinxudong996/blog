循环加载指的是两个脚本互相引用

```
let a = require('./b')
let b = require('./a')
```

循环加载表示存在强耦合，如果处理不好，很容易导致递归加载使得程序无法执行，因此应该尽量避免。然而在较大的项目中很难避免，这就意味着模块加载机制必须要考虑循环加载这个情况。

目前常用的两种模块加载方式CommonJs和ES6,处理方式不一样，返回的结果页不一样。

#### CommonJS模块循环加载

CommonJS模块是Node.js专用的，使用`require()`导入模块，`module.exports`加载模块。这种模块加载核心就是`require`语句，接下来深入的学习下。

##### require加载原理

###### 1.require用法

当Node遇到require(X)时，会按照下面顺序处理：

1. 如果X是内置模块，比如`require('http')`

   返回该模块，不在继续执行

2. 如果X以“./”、"/"、“../”开头

   根据X所在的父模块，确定X的绝对路径，随后将X当成文件一次查找`x、x.js、x.json、x.node`，只要存在其中一个，就返回该文件

3. 如果X不戴路径

   根据X所在的父模块，确定X可能的安装目录，在每个目录中，将X当成文件名或者目录加载

4. 抛出“not found”

###### 2.模块加载原理

CommonJS的一个模块就是一个脚本文件，`require`命令第一次加载该脚本，就会执行整个脚本，随后在内存中生成一个对象。

```javascript
{
  id: '...',
  exports: { ... },
  loaded: true,
  ...
}
```

该对象的`id`属性是模块名，`exports`属性是模块输出的各个接口，`loaded`属性是一个布尔值，表示该模块的脚本是否执行完毕。 

以后需要用到这个模块的时候，就会到`exports`属性上面取值。即使再次执行`require`命令，也不会再次执行该模块，而是到缓存之中取值 

```javascript
//a.js
var counter = 3;
function incCounter() {
  counter++;
  console.log("当前的counter值：" + counter)
}
module.exports = {
  counter: counter,
  incCounter: incCounter,
};
```

```javascript
//b.js
var mod = require('./a');

console.log(mod.counter);  // 3
mod.incCounter();
console.log(mod.counter); // 3
```

在命令行运行`node b.js`，控制台打印：

```
3
当前的counter值：4
3
```

`b.js`模块加载后，就会被缓存到内存中，后续取值并不会重新加载模块，而是从内存中取值。

#### ES6循环加载

CommonJS模块在加载时才会执行脚本，即`require`时执行代码。一旦某个模块被循环加载，就只输出已经执行的部分，还未执行的部分不会输出。

看一个官网上的例子：

```javascript
//a.js
console.log('a starting');
exports.done = false;
const b = require('./b.js');
console.log('in a, b.done = %j', b.done);
exports.done = true;
console.log('a done');
```

```javascript
// b.js：
console.log('b starting');
exports.done = false;
const a = require('./a.js');
console.log('in b, a.done = %j', a.done);
exports.done = true;
console.log('b done');
```

```javascript
//main.js
console.log('main starting');
const a = require('./a.js');
const b = require('./b.js');
console.log('in main, a.done = %j, b.done = %j', a.done, b.done);
```

运行`main.js`，输出：

```
main starting
a starting
b starting
in b, a.done = false
b done
in a, b.done = true
a done
in main, a.done = true, b.done = true
```

在`main.js`中首先加载`a.js`，执行`a.js`脚本，打印`a starting`，导出`done=false`，随后加载b脚本，在这里会等到b脚本全部执行完毕后才会回到这里继续执行；在b脚本中同样导出`done=false`，就加载a脚本，这里发生了循环引用，就只会拿到a脚本已经加载的部分，即`done=false`，随后执行完b脚本，回到引入b脚本这里继续执行a脚本，a脚本执行完毕后就回到了`main.js`中，此时a和b都已经执行完毕了，所以结果都是true。



ES6模块的循环加载

ES6模块是动态引用，不存在缓存值的问题，它遇到模块加载命令`import`时，不会去执行模块，而是只生成一个引用。等到真的需要用到时，再到模块里面去取值。 

```javascript
//m.js
import {foo} from './n.js';
console.log(foo);
setTimeout(() => console.log(foo), 500);
```

```javascript
//n.js
export var foo = 'bar';
setTimeout(() => foo = 'baz', 500);
```

运行`n.js`，随后即可看到先打印bar，0.5s后打印baz。

ES6模块不会缓存运行结果，而是动态地去被加载的模块取值，以及变量总是绑定其所在的模块。也就说ES6模块根本不会关心是否发生了"循环加载"，只是生成一个指向被加载模块的引用，需要开发者自己保证，真正取值的时候能够取到值。











