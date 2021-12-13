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







#### 函数组合