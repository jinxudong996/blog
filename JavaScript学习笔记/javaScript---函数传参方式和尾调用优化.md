##### 传参方式

> ECMAScript中所有函数的参数都是按值传递的。也就是说，把函数外部的值复制给函数内部的参数，就和把值从一个变量复制到另一个变量一样。 
>

###### 按值传递

```javascript
var name = 'nick';
function foo(v) {
    v = 'tom';
    console.log(v); //tom
}
foo(name);
console.log(name) //nick
```

当传递 name到函数 foo 中，相当于拷贝了一份 name，假设拷贝的这份叫 _name，函数中修改的都是 _name的值，而不会影响原来的 name值 

###### 引用传递

```javascript
var obj = {
    value: 1
};
function foo(o) {
    o.value = 2;
    console.log(o.value); //2
}
foo(obj);
console.log(obj.value) // 2
```

###### 共享传递

```javascript
var obj = {
    value: 1
};
function foo(o) {
    o = 2;
    console.log(o); //2
}
foo(obj);
console.log(obj.value) // 1
```

而共享传递是指，在传递对象的时候，传递对象的引用的副本。所以修改 o.value，可以通过引用找到原值，但是直接修改 o，并不会修改原值。所以第二个和第三个例子其实都是按共享传递。 

所以javascript函数传参实际上是：参数如果是基本类型是按值传递，如果是引用类型按共享传递。



##### 尾调用优化

ECMAScript 6 规范新增了一项内存管理优化机制，让 JavaScript 引擎在满足条件时可以重用栈帧。 具体来说，这项优化非常适合“尾调用”，即外部函数的返回值是一个内部函数的返回值。比如： 

```
function outerFunction() {
  return innerFunction(); // 尾调用
}
```

 (1) 执行到 outerFunction 函数体，第一个栈帧被推到栈上。

 (2) 执行 outerFunction 函数体，到 return 语句。计算返回值必须先计算 innerFunction。

 (3) 执行到 innerFunction 函数体，第二个栈帧被推到栈上。 

 (4) 执行 innerFunction 函数体，计算其返回值。

 (5) 将返回值传回 outerFunction，然后 outerFunction 再返回值。

 (6) 将栈帧弹出栈外。

 在 ES6 优化之后，执行这个例子会在内存中发生如下操作。

 (1) 执行到 outerFunction 函数体，第一个栈帧被推到栈上。 

 (2) 执行 outerFunction 函数体，到达 return 语句。为求值返回语句，必须先求值 innerFunction。 

 (3) 引擎发现把第一个栈帧弹出栈外也没问题，因为 innerFunction 的返回值也是 outerFunction 的返回值。 

 (4) 弹出 outerFunction 的栈帧。 

 (5) 执行到 innerFunction 函数体，栈帧被推到栈上。 

 (6) 执行 innerFunction 函数体，计算其返回值。 

 (7) 将 innerFunction 的栈帧弹出栈外。 

很明显，第一种情况下每多调用一次嵌套函数，就会多增加一个栈帧。而第二种情况下无论调用多 少次嵌套函数，都只有一个栈帧。这就是 ES6 尾调用优化的关键：如果函数的逻辑允许基于尾调用将其销毁，则引擎就会那么做。 

尾调用由于是函数的最后一步操作，所以不需要保留外层函数的调用帧，因为调用位置、内部变量等信息都不会再用到了，只要直接用内层函数的调用帧，取代外层函数的调用帧就可以了。

###### 尾递归

函数调用自身，称为递归。如果尾调用自身，就称为尾递归。

递归非常耗费内存，因为需要同时保存成千上百个调用帧，很容易发生“栈溢出”错误（stack overflow）。但对于尾递归来说，由于只存在一个调用帧，所以永远不会发生“栈溢出”错误。   

```
function factorial(n) {
  if (n === 1) return 1;
  return n * factorial(n - 1);
}
```

上面代码是一个阶乘函数，计算`n`的阶乘，最多需要保存`n`个调用记录，复杂度 O(n) 

```
function factorial(n, total) {
  if (n === 1) return total;
  return factorial(n - 1, n * total);
}
```

 如果改写成尾递归，只保留一个调用记录，复杂度 O(1) 。 

 通过递归 计算斐波纳契数列的函数： 

```javascript
function fib(n) {
 if (n < 2) {
 return n;
 }
 return fib(n - 1) + fib(n - 2);
}
console.log(fib(0)); // 0
console.log(fib(1)); // 1
console.log(fib(2)); // 1
console.log(fib(3)); // 2
console.log(fib(4)); // 3
console.log(fib(5)); // 5
console.log(fib(6)); // 8 
```

尾调用优化

```
function Fibonacci2 (n , ac1 = 1 , ac2 = 1) {
  if( n <= 1 ) {return ac2};

  return Fibonacci2 (n - 1, ac2, ac1 + ac2);
}
```

