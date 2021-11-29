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































