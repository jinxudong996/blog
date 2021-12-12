##### 简介

`WeakMap`与`map`结构类似，用于生成键值对的集合。`JavaScript`对象本质就是键值对的集合，但只能用字符串当做键，`ES6`提供了Map数据结构，它类似于对象，也是键值对的集合，但是“键”的范围不限于字符串，各种类型的值（包括对象）都可以当作键。也就是说，Object 结构提供了“字符串—值”的对应，Map 结构提供了“值—值”的对应，是一种更完善的 Hash 结构实现。 

`WeakMap`只接受对象作为键名，不接受其他类型的值作为健名，包括null。

```javascript
const map = new WeakMap();
map.set(1, 2)
// TypeError: 1 is not an object!
map.set(Symbol(), 2)
// TypeError: Invalid value used as weak map key
map.set(null, 2)
// TypeError: Invalid value used as weak map key
```

`WeakMap`的键名所指向的对象，是个弱引用，不计入垃圾回收机制 。只要所引用对象的其他引用都被清除，垃圾回收机制就会释放改对象所占用的内存。

 WeakMap 弱引用的只是键名，而不是键值。键值依然是正常引用。 

```javascript
const wm = new WeakMap();
let key = {};
let obj = {foo: 1};

wm.set(key, obj);
obj = null;
wm.get(key)
// Object {foo: 1}
```

可以写个node的小demo验证下这个观点：

在命令行运行`node --expose-gc`，表示允许手动执行垃圾回收机制。随后手动执行一次垃圾回收机制，保证获取的内存使用状态准确`global.gc()`，随后运行`process.memoryUsage()`查看运行状态：

```
{
  rss: 21884928,
  heapTotal: 4468736,
  heapUsed: 2797232,
  external: 1685266,
  arrayBuffers: 34509
}
```

随后新建一个WeakMap实例，并保存一个较大的变量，`let wm = new WeakMap();` `let key = newArray(5*1024*1024)` `wm.set(key, 1)`

随后手动清除内存，再次查看内存，可以看到WeakMap对值的引用并没有消失：

```
{
  rss: 54235136,
  heapTotal: 46682112,
  heapUsed: 45074784,
  external: 1685299,
  arrayBuffers: 75462
}
```

而清除key的引用，可以看到`WeakMap`的键名所指向的对象，是个弱引用，不计入垃圾回收机制 。只要所引用对象的其他引用都被清除，垃圾回收机制就会释放改对象所占用的内存。

```
key = null;
global.gc();
process.memoryUsage();
//打印结果
{
  rss: 12255232,
  heapTotal: 4734976,
  heapUsed: 3004776,
  external: 1685290,
  arrayBuffers: 108221
}
```

 WeakMap 与 Map 在 API 上的区别主要是两个，一是没有遍历操作（即没有`keys()`、`values()`和`entries()`方法），也没有`size`属性。  二是无法清空，即不支持`clear`方法。因此，`WeakMap`只有四个方法可用：`get()`、`set()`、`has()`、`delete()`。 

```javascript
const wm = new WeakMap();

// size、forEach、clear 方法都不存在
wm.size // undefined
wm.forEach // undefined
wm.clear // undefined
```



##### 用途

###### 1.存储dom节点

```javascript
let myWeakmap = new WeakMap();

myWeakmap.set(
  document.getElementById('logo'),
  {timesClicked: 0})
;

document.getElementById('logo').addEventListener('click', function() {
  let logoData = myWeakmap.get(document.getElementById('logo'));
  logoData.timesClicked++;
}, false);
```

`document.getElementById('logo')`是一个 DOM 节点，每当发生`click`事件，就更新一下状态。我们将这个状态作为键值放在 WeakMap 里，对应的键名就是这个节点对象。一旦这个 DOM 节点删除，该状态就会自动消失，不存在内存泄漏风险。 

###### 2.保存私有变量

```javascript
const _private = new WeakMap();

class Example {
  constructor() {
    _private.set(this, 'private');
  }
  getName() {
  	return _private.get(this);
  }
}

var ex = new Example();

console.log(ex.getName()); // private
console.log(ex.name); // undefined
```

###### 3.数据缓存

```javascript
const cache = new WeakMap();
function countOwnKeys(obj) {
    if (cache.has(obj)) {
        console.log('Cached');
        return cache.get(obj);
    } else {
        console.log('Computed');
        const count = Object.keys(obj).length;
        cache.set(obj, count);
        return count;
    }
}
```



