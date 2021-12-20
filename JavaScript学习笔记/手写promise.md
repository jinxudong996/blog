#### 简介

promise构造函数返回一个promise对象实例，这个返回的promise对象具有一个then方法，在then方法中有两个参数，分别是onfulfilled和onrejected，他们都是函数类型的参数。其中onfulfilled可以通过参数promise对象获取resolve处理后的值，onrejected可以获取promise对象经过reject处理后的值。通过这个值，我们可以处理异步操作完成后的逻辑。

总结下promise的特性：

1.  Promise 就是一个类 在执行这个类的时候 需要传递一个执行器进去 执行器会立即执行

2. Promise 中有三种状态 分别为 成功 fulfilled 失败 rejected 等待 pending

     pending -> fulfilled

     pending -> rejected

     一旦状态确定就不可更改

3.  resolve和reject函数是用来更改状态的

     resolve: fulfilled

     reject: rejected

4. then方法内部做的事情就判断状态 如果状态是成功 调用成功的回调函数 如果状态是失败 调用失败回调函数 then方法是被定义在原型对象中的

5. then成功回调有一个参数 表示成功之后的值 then失败回调有一个参数 表示失败后的原因

6. 同一个promise对象下面的then方法是可以被调用多次的

7. then方法是可以被链式调用的, 后面then方法的回调函数拿到值的是上一个then方法的回调函数的返回值

#### 编写

##### 核心逻辑

编写一个`myPromise`的类：

```javascript
const PENDING = 'pending'; // 等待
const FULFILLED = 'fulfilled'; // 成功
const REJECTED = 'rejected'; // 失败

class MyPromise {
  constructor(executor) {
    executor(this.resolve, this.reject)
  }

  status = PENDING; //初始状态
  value = '';  //成功状态
  reason = ''; //失败状态

  resolve = (value) => {
    if (this.status !== PENDING) return;
    this.status = FULFILLED;
    this.value = value;
  }

  reject = (value) => {
    if (this.status !== PENDING) return;
    this.value = value;
    this.status = REJECTED;
  }
  then = (successCB, failCB) => {
    if (this.status === FULFILLED) {
      successCB(this.value);
    } else if (this.status === REJECTED) {
      failCB(this.value);
    }
  }
}

module.exports = MyPromise;
```

首先定义了三个全局变量，存储着promise的三种不同的状态，随后定义一个`MyPromise`类，构造函数中传入一个执行器函数，在构造函数中进行调用。定义了三个成员变量：status来保存promise的状态，value和reason来保存执行的结果，分别在resolve和reject中来更改promise的状态，随后在then方法中根据promise的状态来执行不同的回调函数。

验证一下：

