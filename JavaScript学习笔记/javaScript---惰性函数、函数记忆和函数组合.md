#### 惰性函数

需要写一个函数返回首次调用的时间，可以用闭包试下：

```javascript
var foo = (function() {
    var t;
    return function() {
        if (t) return t;
        t = new Date();
        return t;
    }
})();
console.log(foo())
console.log(foo())
console.log(foo())
//2021-12-13T10:22:52.363Z
//2021-12-13T10:22:52.363Z
//2021-12-13T10:22:52.363Z

```

这种也是需要先判断是否有t，可以使用惰性函数来解决每次都需要判断的问题：

```javascript
var foo = function() {
    var t = new Date();
    foo = function() {
        return t;
    };
    return foo();
};
console.log(foo())
console.log(foo())
console.log(foo())
// 2021-12-13T10:25:34.392Z
// 2021-12-13T10:25:34.392Z
// 2021-12-13T10:25:34.392Z

```

这种惰性函数就是重写foo函数，将第一次生成的t返回出去，这就形成了一个闭包，后续每次调用foo实际上执行的就是foo内部的匿名函数，将闭包返回出去。

#### 函数记忆

> 函数记忆是指将上次的计算结果缓存起来，当下次调用时，如果遇到相同的参数，就直接返回缓存中的数据。 

`《JavaScript权威指南》`中写过一个memoize：

```javascript
function memoize(f) {
    var cache = {};
    return function(){
        var key = arguments.length + Array.prototype.join.call(arguments, ",");
        if (key in cache) {
            return cache[key]
        }
        else {
            return cache[key] = f.apply(this, arguments)
        }
    }
}
```

这种就是用一个闭包来存储函数执行的值，key是参数长度和参数组成的字符串，执行函数前先遍历存储对象，如果存在key就返回对象中的值，如果不存在就执行函数并存储在对象中。

因为使用`join`拼接字符串，然而如果是个参数是对象就会出问题，可以更改下：

```javascript
var memoize = function(func, hasher) {
    var memoize = function(key) {
        var cache = memoize.cache;
        var address = '' + (hasher ? hasher.apply(this, arguments) : key);
        if (!cache[address]) {
            cache[address] = func.apply(this, arguments);
        }
        return cache[address];
    };
    memoize.cache = {};
    return memoize;
};
```



#### 函数组合

 我们需要写一个函数，输入 'kevin'，返回 'HELLO, KEVIN'。 

```javascript
var toUpperCase = function(x) { return x.toUpperCase(); };
var hello = function(x) { return 'HELLO, ' + x; };

var greet = function(x){
    return hello(toUpperCase(x));
};

greet('kevin');
```

然而这种由内向外的写法，一旦嵌套层数过多，可读性就会很差，希望改写成从左向右的写法：

```javascript
function compose() {
    var args = arguments;
    var start = args.length - 1;
    return function() {
        var i = start;
        var result = args[start].apply(this, arguments);
        while (i--) result = args[i].call(this, result);
        return result;
    };
};
```

```javascript
var toUpperCase = function(x) { return x.toUpperCase(); };
var hello = function(x) { return 'HELLO, ' + x; };

let a = compose(hello,toUpperCase)
console.log(a('nick'))
```

这种就是取得`compose`参数的最后一个函数，并将执行的结果依次传递给前一位，执行完毕后返回。