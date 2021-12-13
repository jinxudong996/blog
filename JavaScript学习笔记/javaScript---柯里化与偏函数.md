#### 柯里化

柯里化函数：将一个多元函转换成依次调用的单元函数

```javascript
const _ = require('lodash')
// 要柯里化的函数
function getSum (a, b, c) {
	return a + b + c
}
// 柯里化后的函数
let curried = _.curry(getSum)
// 测试
console.log(curried(1, 2, 3)) //6
console.log(curried(1)(2)(3)) //6
console.log(curried(1, 2)(3)) //6
```

##### 用途

```javascript
function ajax(){...}
// 虽然 ajax 这个函数非常通用，但在重复调用的时候参数冗余
ajax('POST', 'www.test.com', "name=kevin")
ajax('POST', 'www.test2.com', "name=kevin")
ajax('POST', 'www.test3.com', "name=kevin")

// 利用 curry
var ajaxCurry = curry(ajax);

// 以 POST 类型请求数据
var post = ajaxCurry('POST');
post('www.test.com', "name=kevin");

// 以 POST 类型请求来自于 www.test.com 的数据
var postFromTest = post('www.test.com');
postFromTest("name=kevin");
```

curry 的这种用途可以理解为：参数复用。本质上是降低通用性，提高适用性。 

同样也可以将柯里化后的函数传给map：

```javascript
var person = [{name: 'kevin'}, {name: 'daisy'}]

var name = person.map(function (item) {
    return item.name;
})

var prop =  curry(function (key, obj) {
    return obj[key]
});

var name = person.map(prop('name'))

console.log(name)
//[ 'kevin', 'daisy' ]
```

##### 仿写

接下来模拟下模拟下curry函数：

```javascript
function curry (func) {
  return function curriedFn (...args) {
    if (args.length < func.length) {
      return function () {
        return curriedFn(...args.concat(Array.from(arguments)))
      }
    }
    return func(...args)
  }
}
```

这个函数首先返回一个函数，以便接受后续参数，先判断形参与实参的数量，假如实参和形参数量相同，就直接执行func（）并返回，假如不等，就返回一个函数，并将实参返回出去，这里就形成了一个闭包，这里将实参存储起来，通过Array.concat函数将实参依次连接起来，直到实参等于形参，再执行func（）。这也算是闭包的一个运用场景。



#### 偏函数

> 在计算机科学中，偏函数是指固定一个函数的一些参数，然后产生另一个更小元的函数。
>
> 什么是元？元是指函数参数的个数，比如一个带有两个参数的函数被称为二元函数。

```javascript
const _ = require('lodash')

function add(a, b) {
    return a + b;
}

// 执行 add 函数，一次传入两个参数即可
add(1, 2) // 3

var addOne = _.partial(add, 1);

console.log(addOne(2)) // 3
```

跟柯里化是很像的，但还是有些区别的：

> 柯里化是将一个多参数函数转换成多个单参数函数，也就是将一个 n 元函数转换成 n 个一元函数。
>
> 偏函数则是固定一个函数的一个或者多个参数，也就是将一个 n 元函数转换成一个 n - x 元函数。

##### 仿写

```javascript
function partial(fn) {
    var args = [].slice.call(arguments, 1);
    return function() {
        var newArgs = args.concat([].slice.call(arguments));
        console.log(arguments)
        return fn.apply(this, newArgs);
    };
};
```

