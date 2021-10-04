

#### 异步及Promise

> 



#### 异步及Promise

先看一个例子：

```JavaScript
setTimeout( () => {
  console.log('100')
},100)

while (true) {

}
console.log('end') 
```

以上代码块不会打印任何l输出，因为while循环会一直执行，主线程被占用。

JavaScript中的任务可以分为同步任务和异步任务：

- 同步任务：当前主线程将要执行的任务，这些任务一起形成一个执行栈，
- 异步任务：不进入主线程，进入任务队列，当主线程的执行栈中的函数全部弹出时才会执行任务队列

异步任务又分为宏任务与微任务，微任务先于宏任务执行。

宏任务有：

- setTimeout
- setInterval
- I/O
- 事件
- postMessage
- requestAnimation
- setImmediate（nodeJs的api）

微任务有：

- Promise.then()
- MutationObserver()
- process.nextTick()

这里的async和awit是个坑啊，还不会。

```JavaScript
console.log('aaa');

(async ()=>{
  console.log(111);
  await console.log(222);
  console.log(333);
})().then(()=>{
  console.log(444);
});

console.log('ddd');
```

扯的有点远了，回到异步来，ES6之前解决异步都是使用回调的形式， 很容易形成层层嵌套的回调函数，也就是回调地狱。ES6加入了Promise，成为了主导的异步编程机制。

> Promise就是一个容器，里面保存着未来某个才会结束的事件（通常是一个异步操作）的结果。

promise的常用语法就不赘述了，笔者都比较熟悉了。

手写promise

1. Promise 就是一个类 在执行这个类的时候 需要传递一个执行器进去 执行器会立即执行

2. Promise 中有三种状态 分别为 成功 fulfilled 失败 rejected 等待 pending

   pending -> fulfilled

   pending -> rejected

   一旦状态确定就不可更改

3. resolve和reject函数是用来更改状态的

   resolve: fulfilled

   reject: rejected

4. then方法内部做的事情就判断状态 如果状态是成功 调用成功的回调函数 如果状态是失败 调用失败回调函数 then方法是被定义在原型对象中的