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

```javascript
const MyPromise = require('./promise');

let p = new MyPromise( (resolve,reject) => {
    resolve('成功。。。')
})

p.then( resolve => {
    console.log(resolve)
}, reject => {
    console.log(reject)
})

//promise成功。。。
```



##### 添加异步逻辑

如果在resolve函数中添加异步代码，这个promise就会出现问题：

```javascript
const MyPromise = require('./promise');

let p = new MyPromise( (resolve,reject) => {
    setTimeout(() => {
        resolve('成功。。。')
    },2000)
})

p.then( resolve => {
    console.log(resolve)
}, reject => {
    console.log(reject)
})
```

这里什么也不会打印，因为resolve()会被添加到异步队列中，先等主线程任务执行完了才会轮到它，也就是先会执行then方法，而then方法中只判断了两种状态，没有判断等待状态，这里在then方法中添加一个等待状态：

```javascript
then = (successCB, failCB) => {
    if (this.status === FULFILLED) {
        successCB(this.value);
    } else if (this.status === REJECTED) {
        failCB(this.value);
    } else {
        //异步  等待状态
        this.successCB = successCB;
        this.failCB = failCB;
    }
}
```

用两个变量存储回调函数，随后根据promise的状态，在有回调的情况下执行回调：

```javascript
resolve = (value) => {
    if (this.status !== PENDING) return;
    this.status = FULFILLED;
    this.value = value;
    //成功回调
    this.successCB && this.successCB(this.value)
}

reject = (value) => {
    if (this.status !== PENDING) return;
    this.value = value;
    this.status = REJECTED;
    //失败回调
    this.failCallback && this.failCallback(this.value)
}
```

验证一下：

```javascript
const MyPromise = require('./promise');

let p = new MyPromise( (resolve,reject) => {
    setTimeout(() => {
        resolve('成功。。。')
    },2000)
})

p.then( resolve => {
    console.log(resolve)
}, reject => {
    console.log(reject)
})

//2s后 打印 成功。。。
```



##### 多次调用then方法

多次调用then方法主要分为同步和异步，同步目前代码已经可以支持了，then方法中会根据不同的状态来执行不同的回调。异步的话，就需要将回调函数存储起来，将resolve中的执行结果分别传入：

```javascript
// 成功回调
  successCB = [];
  // 失败回调
  failCallback = [];
  resolve = (value) => {
    if (this.status !== PENDING) return;
    this.status = FULFILLED;
    this.value = value;
    //成功回调
    // this.successCB && this.successCB(this.value)
    while(this.successCB.length) this.successCB.shift()(this.value)
  }

  reject = (value) => {
    if (this.status !== PENDING) return;
    this.value = value;
    this.status = REJECTED;
    //失败回调
    // this.failCallback && this.failCallback(this.value)
    while(this.failCallback.length) this.failCallback.shift()(this.value)
  }
  then = (successCB, failCB) => {
    if (this.status === FULFILLED) {
      successCB(this.value);
    } else if (this.status === REJECTED) {
      failCB(this.value);
    }else{
      //异步  等待状态
      this.successCB.push(successCB);
      this.failCallback.push(failCB);
    }
  }
```

定义两个成员变量来存储回调函数，执行then方法中依次将回调加入成员变量中，随后分别在resolve和reject中执行回调，执行回调时利用while遍历数组，shift返回第一个元素，也就是根据加入的顺序依次执行。

验证一下：

```javascript
let p = new MyPromise( (resolve,reject) => {
    setTimeout(() => {
        reject('成功。。。')
    },2000)
})

p.then( resolve => {
    console.log(resolve)
}, reject => {
    console.log(reject)
})
p.then( resolve => {
    console.log(resolve)
}, reject => {
    console.log(reject)
})
//成功。。。
//成功。。。
```

##### then方法的链式调用

实现then方法的链式调用，首先需要在then方法中返回一个promise对象，随后再判断是普通值还是promise对象，如果是普通值，直接将值传递给新promise对象的resolve方法即可，如果是promise对象，就需要判断promise对象的状态，如果是成功就需要将值传递给resolve方法，失败的话传递给reject方法。

```javascript
then = (successCB, failCB) => {
    let p2 =  new MyPromise((resolve,reject) => {
      if (this.status === FULFILLED) {
        let x = successCB(this.value);
        // resolve(x)
        resolvePromise(x,resolve,reject)
      } else if (this.status === REJECTED) {
        failCB(this.value)
      }else{
        //异步  等待状态
         this.successCB.push(successCB);
         this.failCallback.push(failCB);
      }
    })
    return p2
  }
```

```javascript
function resolvePromise (x, resolve, reject) {
  if (x instanceof MyPromise) {
    // promise 对象
    x.then(resolve, reject);
  } else {
    // 普通值
    resolve(x);
  }
}
```

##### promise.all实现

promise.all()用来解决异步并发问题的，允许我们以异步调用的顺序来得到异步执行的结果。该方法属于静态方法，接受一个数组作为参数，返回结果也是一个数组，数组中的内容就是根据函数调用顺序排列的。

```javascript
static all (array) {
    let result = [];
    let index = 0;
    return new MyPromise((resolve, reject) => {
      function addData (key, value) {
        result[key] = value;
        index++;
        if (index === array.length) {
          resolve(result);
        }
      }
      for (let i = 0; i < array.length; i++) {
        let current = array[i];
        if (current instanceof MyPromise) {
          // promise 对象
          current.then(value => addData(i, value), reason => reject(reason))
        }else {
          // 普通值
          addData(i, array[i]);
        }
      }
    })
  }
```

因为使用promise.all后续都是接的then方法，所以在内部就返回一个promise对象。在对象中申明了一个addDate方法，用来按照参数列表的顺序来排列函数执行的结果。在函数内部有一个判断，每次向result数组塞一个值就+1，直到该值与参数列表相等，表明所有的函数均已经执行完毕，再讲result抛给then。

[代码地址](https://github.com/jinxudong996/blog/blob/main/JavaScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/code/promise/promise.js)