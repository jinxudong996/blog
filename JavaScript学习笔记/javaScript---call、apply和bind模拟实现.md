#### call

>  call() 方法在使用一个指定的 this 值和若干个指定的参数值的前提下调用某个函数或方法。 

```javascript
function sub() {
    this.color = ['red','green']
}
function sup() { 
    // 此处this指向sup新实例，在新实例中调用sub（）
    sub.call(this)
}

let sup1 = new sup()

sup1.color.push('black')
console.log(sup1.color) //["red", "green", "black"]

let sup2 = new sup()
console.log(sup2.color) //["red", "green"]
```

比如这种盗用构造函数的继承方式，在构造函数中内部调用`sub.call(this)`，this指向由`sup`创建的新实例，这就相当于将`sub`挂载到新实例上。

主要两点

- call改变了this的指向
- 执行了绑定的函数

##### 模拟实现

```javascript
Function.prototype.call2 = function(context) {
// 首先要获取调用call的函数，用this可以获取
    context.fn = this;
    context.fn();
    delete context.fn;
}

var foo = {
    value: 1
};

function bar() {
    console.log(this.value);
}

bar.call2(foo); // 1
```

首先改变this的指向，我们将bar设置为foo的一个方法，就像这样

```javascript
foo:{
	bar:function(){}
}
```

这样bar中this的始终指向foo，随后在调用下bar，再利用`delete`删除这个方法，这样就实现了`call`方法。

改写下盗用构造函数的继承方式：

```javascript
Function.prototype.call2 = function(context) {
    context.fn = this;
    context.fn();
    delete context.fn;
}
function sub() {
    this.color = ['red','green']
}
function sup() { 
    // 此处this指向sup新实例，在新实例中调用sub（）
    sub.call2(this)
}

let sup1 = new sup()

sup1.color.push('black')
console.log(sup1.color) //["red", "green", "black"]

let sup2 = new sup()
console.log(sup2.color) //["red", "green"]
```

然而正宗的`call`还可以接受不定参数的，也就是接受参数的个数不受限制，可以用到`arguments`属性来获取传入`call2`的参数列表，改写如下：

```javascript
Function.prototype.call2 = function(context) {
    context.fn = this;
    var args = [];
    for(var i = 1, len = arguments.length; i < len; i++) {
        args.push(arguments[i]);
    }
    context.fn(...args)
    delete context.fn;
}
```

因为传入的参数列表中第一个是绑定this的目标对象，所以拿到第二个往后的参数，并依次传入。

在用使用call中经常遇到第一个参数传入`null`的，这是this就会指向`window`。还有一点，函数可以是有返回值的，接下来改进下

```javascript
Function.prototype.call2 = function (context) {
    var context = context || window;
    context.fn = this;

    var args = [];
    for(var i = 1, len = arguments.length; i < len; i++) {
        args.push(arguments[i]);
    }
    
    var result = context.fn(...args);

    delete context.fn
    return result;
}
```



#### apply

apply与call基本类似，区别在于apply的第二个参数是一个数组，有了call的经验，apply就比较简单了

```javascript
Function.prototype.apply = function (context, arr) {
    var context = Object(context) || window;
    context.fn = this;

    var result;
    if (!arr) {
        result = context.fn();
    }
    else {
        var args = [];
        for (var i = 0, len = arr.length; i < len; i++) {
            args.push(arr[i]);
        }
        result = context.fn(...args)
    }

    delete context.fn
    return result;
}
```



#### bind

> bind() 方法会创建一个新函数。当这个新函数被调用时，bind() 的第一个参数将作为它运行时的 this，之后的一序列参数将会在传递的实参前传入作为它的参数 

##### 用法

`bind()` 最简单的用法是创建一个函数，不论怎么调用，这个函数都有同样的 **`this`** 值。JavaScript新手经常犯的一个错误是将一个方法从对象中拿出来，然后再调用，期望方法中的 `this` 是原来的对象（比如在回调中传入这个方法）。如果不做特殊处理的话，一般会丢失原来的对象。基于这个函数，用原始的对象创建一个绑定函数，巧妙地解决了这个问题： 

```javascript
this.x = 9;    // 在浏览器中，this 指向全局的 "window" 对象
var module = {
  x: 81,
  getX: function() { return this.x; }
};

module.getX(); // 81

var retrieveX = module.getX;
retrieveX();
// 返回 9 - 因为函数是在全局作用域中调用的

// 创建一个新函数，把 'this' 绑定到 module 对象
// 新手可能会将全局变量 x 与 module 的属性 x 混淆
var boundGetX = retrieveX.bind(module);
boundGetX(); // 81
```



`bind()` 的另一个最简单的用法是使一个函数拥有预设的初始参数。只要将这些参数（如果有的话）作为 `bind()` 的参数写在 `this` 后面。当绑定函数被调用时，这些参数会被插入到目标函数的参数列表的开始位置，传递给绑定函数的参数会跟在它们后面。 

```javascript
function list() {
  return Array.prototype.slice.call(arguments);
}

function addArguments(arg1, arg2) {
    return arg1 + arg2
}

var list1 = list(1, 2, 3); // [1, 2, 3]

var result1 = addArguments(1, 2); // 3

// 创建一个函数，它拥有预设参数列表。
var leadingThirtysevenList = list.bind(null, 37);

// 创建一个函数，它拥有预设的第一个参数
var addThirtySeven = addArguments.bind(null, 37);

var list2 = leadingThirtysevenList();
// [37]

var list3 = leadingThirtysevenList(1, 2, 3);
// [37, 1, 2, 3]

var result2 = addThirtySeven(5);
// 37 + 5 = 42

var result3 = addThirtySeven(5, 10);
// 37 + 5 = 42 ，第二个参数被忽略
```



绑定函数自动适应于使用 [`new`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/new) 操作符去构造一个由目标函数创建的新实例。当一个绑定函数是用来构建一个值的，原来提供的 `this` 就会被忽略。不过提供的参数列表仍然会插入到构造函数调用时的参数列表之前 :

```javascript
function Point(x, y) {
  this.x = x;
  this.y = y;
}

Point.prototype.toString = function() {
  return this.x + ',' + this.y;
};

var p = new Point(1, 2);
p.toString(); // '1,2'

var emptyObj = {};
var YAxisPoint = Point.bind(emptyObj, 0/*x*/);

// 本页下方的 polyfill 不支持运行这行代码，
// 但使用原生的 bind 方法运行是没问题的：

var YAxisPoint = Point.bind(null, 0/*x*/);

/*（译注：polyfill 的 bind 方法中，如果把 bind 的第一个参数加上，
即对新绑定的 this 执行 Object(this)，包装为对象，
因为 Object(null) 是 {}，所以也可以支持）*/

var axisPoint = new YAxisPoint(5);
axisPoint.toString(); // '0,5'

axisPoint instanceof Point; // true
axisPoint instanceof YAxisPoint; // true
new YAxisPoint(17, 42) instanceof Point; // true
```



##### 模拟实现

`bind`函数主要有两个特点：

- 返回一个函数
- 可以传参

```javascript
Function.prototype.bind2 = function (context) {

    var self = this;
    // 获取bind2函数从第二个参数到最后一个参数
    var args = Array.prototype.slice.call(arguments, 1);

    return function () {
        // 这个时候的arguments是指bind返回的函数传入的参数
        var bindArgs = Array.prototype.slice.call(arguments);
        return self.apply(context, args.concat(bindArgs));
    }

}

var foo = {
    value: 1
};

function bar(name, age) {
    console.log(this.value);
    console.log(name);
    console.log(age);

}

var bindFoo = bar.bind(foo, 'daisy');
bindFoo('18');
//1
//daisy
//18
```

这里首先保存了this的指向，这里的this就是调用`bind2`函数的方法，也就是我们要绑定的函数，然后根据`arguments`来获得传入的参数,在返回函数中，再次获取传入的参数，利用`concat`合并成新的数组传入要绑定的函数。



当返回的函数当做一个构造函数时，绑定的this会失效，this会指向新的实例，可以使用`this instanceof fBound`来判断`fBound`是否当成了构造函数，

```javascript
Function.prototype.bind2 = function (context) {
    var self = this;
    var args = Array.prototype.slice.call(arguments, 1);

    var fBound = function () {
        var bindArgs = Array.prototype.slice.call(arguments);
        // 当作为构造函数时，this 指向实例，此时结果为 true，将绑定函数的 this 指向该实例，可以让实例获得来自绑定函数的值
        // 当作为普通函数时，this 指向 window，此时结果为 false，将绑定函数的 this 指向 context
        return self.apply(this instanceof fBound ? this : context, args.concat(bindArgs));
    }
    // 修改返回函数的 prototype 为绑定函数的 prototype，实例就可以继承绑定函数的原型中的值
    fBound.prototype = this.prototype;
    return fBound;
}
```













