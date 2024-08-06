#### promsie并发及控制并发详解

前段时间做了个爬虫的需求，用的nodeJs写的，写之前网上找了很多爬虫框架，发现没啥好用的，Puppeteer蛮不错的，就是用起来有点繁琐，适合爬页面，我只需要一个简单好用的爬接口的框架就行，最后无奈自己写了个脚本， 立个flag，后续看能不能自己试着去写一个爬虫框架。

在写脚本的时候，对promise的使用有了更加深刻的理解，大量的接口请求，必然涉及到并发操作，同时网站也有的反爬虫，也会涉及到控制并发的频率，接下里记录下promise的并发和控制并发。

##### 并发操作

提到并发操作，就会想到`promise.all`，这个方法返回一个promise，参数接受一个`promise`数组，当所有的promise数组有结果了之后，返回的promise才会有结果：当所有的promise变成 fulfilled或者有个一promise变成 rejected ，返回的promise就会分别变成fulfilled和rejected。

接下来试着手写下`promise.all`，这也是一个常规的八股文。

###### 手写promise.all

```JavaScript
class MyPromise {
    static all(promises) {
        return new Promise((resolve, reject) => {
            const results = [];
            let completedCount = 0;

            for (let i = 0; i < promises.length; i++) {
                promises[i]
                    .then(result => {
                        results[i] = result;
                        completedCount++;

                        if (completedCount === promises.length) {
                            resolve(results);
                        }
                    })
                    .catch(reject);
            }
        });
    }
}
```

其实还是比较简单的，就是在all函数中返回一个promise，申明一个数组来做存储结果，申明一个变量来计算当前已有结果的数量，当completedCount的和results的长度一样时，表明所有传入的都已经有了计算结果。

###### 手写promise.allSettled

当时在做爬虫时，一旦某个请求出了意外，比如超时，我们的并发就会立即停止，剩余的请求就不会有结果，这显然不是我们想要的，这时就会有`promise.allSettled`这个api来处理这种情况，它的用法和`promise.all`一样，不同的是： `Promise.allSettled` 不会在任何一个 Promise 失败时立即拒绝，而是会等待所有 Promise 都完成后才会返回结果。 

用法实例：

```JavaScript
const promises = [
  Promise.resolve(1),
  Promise.reject("Error"),
  Promise.resolve("Success")
];

Promise.allSettled(promises)
  .then(results => {
    results.forEach(result => {
      if (result.status === "fulfilled") {
        console.log("Promise fulfilled:", result.value);
      } else if (result.status === "rejected") {
        console.log("Promise rejected:", result.reason);
      }
    });
  })
  .catch(error => {
    console.log("Error:", error);
  });
```

要试着手写的话，也比较简单的

```JavaScript
function promiseAllSettled(promises) {
  return Promise.all(promises.map(promise => {
    return promise
      .then(value => ({ status: 'fulfilled', value }))
      .catch(reason => ({ status: 'rejected', reason }));
  }));
}
```

利用`promise.all`，将传入的promises遍历下，fulfilled时返回value，rejected时返回reason

##### 控制并发频率

反爬虫有个最简单的逻辑就是同一IP短时间内出现了高频率的请求，这就需要爬虫添加代理IP和限制并发的频率了，代理IP其实也比较简单，可以找第三方的IP供应商，这里主要探讨的就是控制并发的频率。这里总结了两个限制并发的方法，先看第一个：

```javascript
class MyPLimit {
  constructor(concurrency) {
    this.concurrency = concurrency; // 最大并发数
    this.queue = []; // 任务队列
    this.activeCount = 0; // 当前活跃的任务数
  }

  // 生成随机延迟时间
  generateRandomDelay() {
    return Math.floor(Math.random() * 5000); // 生成 0 到 1000 毫秒之间的随机延迟
  }

  // 添加异步任务到队列中
  async enqueue(fn) {
    return new Promise((resolve, reject) => {
      const task = async () => {
        try {
          const result = await fn();
          resolve(result);
        } catch (error) {
          reject(error);
        } finally {
          this.activeCount--;
          this.processQueue(); // 处理队列中的下一个任务
        }
      };

      if (this.activeCount < this.concurrency) {
        this.activeCount++;
        setTimeout(() => {
          task();
        }, this.generateRandomDelay()); // 添加随机延迟
      } else {
        this.queue.push(task);
      }
    });
  }

  // 处理队列中的下一个任务
  processQueue() {
    if (this.queue.length > 0 && this.activeCount < this.concurrency) {
      const nextTask = this.queue.shift();
      if (nextTask) {
        this.activeCount++;
        setTimeout(() => {
          nextTask();
        }, this.generateRandomDelay()); // 添加随机延迟
      }
    }
  }
}
```

这里实现了一个限制并发任务数量的类`MyPLimit`。它的构造函数接受一个参数`concurrency`，表示最大并发数。它有三个属性：`concurrency`表示最大并发数，`queue`表示任务队列，`activeCount`表示当前活跃的任务数。

类中定义了三个方法：

1. `generateRandomDelay()`方法用于生成一个随机的延迟时间，范围在0到5000毫秒之间。
2. `enqueue(fn)`方法用于将异步任务添加到队列中。它返回一个Promise对象，表示任务的执行结果。该方法内部创建了一个`task`函数，该函数会在执行完任务后，将`activeCount`减1，并调用`processQueue()`方法处理队列中的下一个任务。如果当前活跃的任务数小于最大并发数，就会立即执行任务，并设置一个随机延迟时间。否则，将任务添加到队列中。
3. `processQueue()`方法用于处理队列中的下一个任务。如果队列不为空且当前活跃的任务数小于最大并发数，就会取出队列中的下一个任务并执行，同样设置一个随机延迟时间。

这个方法是自己在爬虫脚本中所使用的，后面自己有网上找了另外一个，是神光大佬写的，实际上基本原理都差不多，都是维护一个队列，一进一出，代码如下：

```javascript
const pLimit = (concurrency) => {  
    const queue = [];
    let activeCount = 0;
  
    const next = () => {
      activeCount--;
  
      if (queue.length > 0) {
        queue.shift()();
      }
    };
  
    const run = async (fn, resolve, ...args) => {
      activeCount++;
  
      const result = (async () => fn(...args))();

      resolve(result);
  
      try {
        await result;
      } catch {}

      next();
    };
  
    const enqueue = (fn, resolve, ...args) => {
      queue.push(run.bind(null, fn, resolve, ...args));
  
      if (activeCount < concurrency && queue.length > 0) {
          queue.shift()();
      }
    };
  
    const generator = (fn, ...args) =>
      new Promise((resolve) => {
        enqueue(fn, resolve, ...args);
      });
  
    return generator;
};
```

