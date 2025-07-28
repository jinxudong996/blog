

##### 引言

写这边文章的契机也是最近在业务开发中遇到了页面卡顿的情形：在正常的业务流程中，随着数据量的变大，原本顺畅的网页突然变得非常卡顿，浏览器的tab页面一直在转圈，但是页面的操作什么都做不了，也就是一种假死状态，只能等待转圈结束，到底是内存泄漏，亦或者是主线程阻塞，写这篇文章总结下Memory 面板的常见用法，以及网页卡顿在内存方向的排查方案。

本文的目标是通过 Chrome DevTools 的 Memory 面板，帮助你掌握 Web 端内存分析的基本方法。我们将从基础概念入手，逐步深入到实际工具使用，并结合一个简单的代码示例进行演示。通过这篇文章，你将学会如何捕获内存快照、识别泄漏源头，并应用到自己的项目中优化性能。

##### 基础概念

###### 内存管理基础

 JavaScript 内存管理遵循 **分配 → 使用 → 释放** 的流程：

- **分配**：变量、对象、数组等数据被创建时，内存自动分配。

  ```js
  let obj = { name: "Test" }; // 内存分配
  ```

- **使用**：程序读取或修改已分配的内存。

  ```js
  console.log(obj.name); // 内存使用
  ```

- **释放**：当数据不再被引用时，垃圾回收（GC）自动回收内存。

  ```js
  obj = null; // 解除引用，等待GC回收
  ```

###### 垃圾回收（GC）机制

 JavaScript 使用自动垃圾回收（Garbage Collection，GC）机制来管理内存，这意味着开发者通常不需要手动分配和释放内存，其内部会通过v8引擎自动追踪内存的分配和使用，当确定某个对象不在被需要时，也就是对象的引用不再被使用时，就会自动释放其占用的内存。

常见的垃圾回收算法主要有两种

1. 标记-清除法

   标记-清除算法分为两个阶段：标记阶段规划和清除阶段，在标记阶段会从根对象，比如全局变量、当前执行栈中的变量等开始遍历，递归的标记所有的可达对象为存活状态；在清除阶段，会遍历整个内存堆，回收所有未被标记的对象占用的内存空间，清除所有对象的标记，来为下一轮的GC做准备。

   一般GC的执行时机和事件循环（Event Loop）没什么关系，独立于事件循环之外，通常会发生在主线程的`call stack`的时候，比如微任务和宏任务之间，当堆内存接近上限时也会触发GC，在浏览器中也可以显示的调用：

   ```js
   if (window.gc) {
     window.gc();
   }
   ```

   

2. 引用计数法

   这是一种简单的垃圾回收策略，它通过跟踪每个对象的引用次数来决定是否回收内存，为每个对象维护一个引用计数器，记录当前有多少变量或者数据结构引用它，当引用计数变为0时，说明该对象不再被任何变量引用，可以立即回收其内存。

###### 内存泄漏的定义

内存泄漏一般是指变量的内存无法被垃圾回收机制回收，导致内存占用持续增长。一般表现就是页面卡顿，响应变慢、浏览器标签内存占用持续上升、频繁的触发GC

比如看下这个例子：

```js
window.leakingArray = [];

function createLeakingObject() {
  const largeObject = {
    data: new Array(100000).fill("leak data"), // Large array to consume memory
    timestamp: new Date(),
  };
  window.leakingArray.push(largeObject); // Push to global array, preventing GC
  console.log(
    "Leaking object created. Current array size:",
    window.leakingArray.length
  );
}

document
  .getElementById("leakButton")
  .addEventListener("click", createLeakingObject);
```

`createLeakingObject`方法被添加到点击事件上，方法内部会创建一个超大的叔祖，将它绑定到全局变量上，因为有这个全局变量的引用，每次点击都会创建很大的对象，但是又不会被GC清除，就会导致内存占用持续上升，直至浏览器崩溃。

接下来通过`Memory 面板`来分析下这个案例：

首先打开控制台（F12），选择Memory面板， 选择 `Heap snapshot（堆快照）`，点击底部Take snapshot 按钮， 就会生成一个快照，然后分别多点击几次按钮，生成对应的快照，如下图

![1753713976967](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1753713976967.png)

如上图，一共生成了8张快照，最后一次堆内存50.4M，而最后一次快照的右侧，还有这样几列，接下来依次介绍：

1.  constructor    

    constructor（构造函数）这一栏显示了每个对象的构造函数名称，也就是该对象是通过哪个构造函数（或类）创建出来的。 通过这一列，可以看到到底是那些对象占据了大量的内存，比如这里的window对象、数组，对象`{data,timestamp}`都和我们主动的内存泄漏操作有关

2.  Distance 

    Distance（距离）表示该对象到“根对象”（Root，如 window 或全局作用域对象）的最短引用路径上的长度，  它反映了对象离根的远近。距离越小，说明对象越容易被全局或主线程引用，越不容易被垃圾回收。 

3.  Shallow Size 

   Shallow Size（浅层大小）是指该对象本身直接占用的内存大小，不包括它引用的其他对象。反映单个对象本身的内存消耗。

4.  Retained Size 

   Retained Size（保留大小）是指如果该对象被垃圾回收，那么连带着所有只能通过它访问到的对象也会被回收，总共能释放的内存大小。它等于该对象本身的 Shallow Size 加上所有只被它引用的对象的 Shallow Size 之和。 基本上我们查找内存泄漏，主要是通过这个数据来看就行了。

通过查看第八张快照的4列，就可以非常容易的定位到内存增长的原因：就是window对象上绑定的数组，后续重点排查相关代码。

###### Memory面板的作用

接下来总结下该面板的作用

1. 分析`JavaScript`堆内存

   可以在快照中的`constructor`列，查看当前内存较大的对象类型，比如Array，后续就可以重点排查对应代码

2. 追踪内存分配与释放

    通过时间线工具观察内存分配的时间点 

   以上面的例子，选择` Allocation  on timeline `（就是上面选择Heap snapshot下面），点击左上角的录制，就开始生成曲线，然后开始页面的操作，比如点击按钮，再次点击左上角的停止按钮，就会生成内存快照

   ![1753716116812](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1753716116812.png)

   横轴是时间，纵轴就是内存，还可以拖动时间轴查看某个峰值的具体情况

3. 识别内存泄漏和性能瓶颈

   



##### Memory面板核心功能

打开Memoty面板，就可以看到 `select profiling type`，选择分析类型，有四个选项，接下来详细介绍下

######  Heap Snapshot（堆快照）

 静态分析某一时刻的 JavaScript 堆内存状态，查看对象分布及引用关系 。这个前面已经演示过了，可以非常方便的分析处内存占用高的对象。

######  Allocation instrumentation on timeline(内存分配时间线)

动态记录内存分配的时间线，定位高频内存分配点。 可以分析代码中那些操作导致内存激增，可以结合 Performance 面板，找到内存分配与页面卡顿的关联。

前面的例子太过简单了，向全局变量上挂载一个大数组，然而在开发过程中，最容易写的还是闭包

看下这个例子，

```js
leakBtn.addEventListener("click", () => {
  // 创建一个大数据对象 - 使用不同的对象避免引擎优化
  let bigData = [];
  for (let i = 0; i < 1000000; i++) { 
    bigData.push({
      id: i,
      data: `这是第${i}个数据对象`,
      timestamp: Date.now(),
      randomValue: Math.random()
    });
  }

  // 创建一个闭包，无意中引用了bigData
  leakedClosure = (function () {
    return function () {
      log(`闭包执行: 数组长度 = ${bigData.length}`);
    };
  })();

  log(`创建了一个包含 ${bigData.length} 个不同对象的数组`);
  log("闭包保留了对整个数组的引用，导致内存泄漏");
  log(`当前数组占用内存: 约 ${(bigData.length * 100 / 1024 / 1024).toFixed(2)} MB`);
});
```

在一个点击事件中，创建一个大的数组对象，然后返回函数中将内部变量return出去，当这个函数在调用栈中执行完后，理论上来说调用栈中的函数执行完成后，会从栈中弹出，函数中的内部变量都会被GC回收，但是在返回函数中bigData被使用了，而且return出去了，bigData就跳出了当前的作用域链，因为有引用的存在，他就不会被GC回收，这个bigData就是闭包，造成了内存泄漏。

打开Memory面板，选择`Allocation instrumentation on timeline`，点击左上角的开始按钮，然后不停的触发`click`点击方法，然后就停止录制。

![1753720124860](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1753720124860.png)

因为过于卡顿，就导致没有生成有意义的曲线，这个搜了下资料也是正常的，在constructor这一列中可以看到内存站占用最大的就是函数类型，打开函数类型，就可以看到函数调用的地方，这就直接定位到了内存泄漏的地方了，非常方便。

###### Allocation Sampling(采样内存分配)

 低开销统计内存分配的来源（按函数分类），适合长时间运行的分析。 

同样使用前面闭包的例子来看一下：步骤都差不多，选择`Allocation Sampling`，点击开始录制，就开始页面操作，一段时间后结束，生成快照。这个不需要精确到每次分配，只需了解哪些函数占用了大部分内存 ，速度就快乐很多，也流畅了很多

![1753720516218](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1753720516218.png)

因为这里只有一个函数，而且点击右侧的调用栈，也可以非常精准的定位到内存泄漏的地方。

###### Detached elements( 分离的 DOM 元素 )

 Detached Elements是指那些已经从 DOM 树中移除（不再显示在页面上），但仍然被 JavaScript 代码保留引用的 DOM 元素 

看下这个案例：

```js
function createLargeElement() {
  const element = document.createElement("div");
  element.className = "big-box";
  element.innerHTML = "<h3>大型数据容器</h3>";

  const largeData = generateLargeData();
  const fragment = document.createDocumentFragment();

  largeData.forEach((item) => {
    const div = document.createElement("div");
    div.className = "data-item";
    div.textContent = `${item.id}: ${item.content.substring(0, 50)}...`;
    fragment.appendChild(div);
  });

  element.appendChild(fragment);
  return element;
}

document.getElementById("create-global").addEventListener("click", () => {
  // 创建大型元素并添加到DOM
  globalElement = createLargeElement();
  document.body.appendChild(globalElement);

  // 3秒后从DOM移除，但全局变量仍保留引用
  setTimeout(() => {
    globalElement.remove();
    document.getElementById("global-info").textContent =
      "大型元素已从DOM移除（约2MB内存），但全局变量 globalElement 仍然引用它。这是一个明显的分离DOM元素。";
    document.getElementById("global-info").style.color = "red";
  }, 3000);
});

document.getElementById("clean-global").addEventListener("click", () => {
  globalElement = null;
  document.getElementById("global-info").textContent =
    "全局引用已设置为null，大型分离的DOM元素（约2MB内存）现在可以被垃圾回收。";
  document.getElementById("global-info").style.color = "green";

  // 建议手动触发GC来观察效果（仅用于演示）
  if (window.gc) {
    window.gc();
    console.log("手动触发垃圾回收");
  }
});
```

观测步骤都大差不差，直接看下生成的快照

![1753721696944](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1753721696944.png)

可以看到有一万的游离的dom节点，点击节点就可以看到节点的详情

##### 内存分析关键指标

###### 内存统计术语

在前面内存泄漏定义那一块已经介绍过了，这里再次回顾下，就是快照上面的一些指标

- **Shallow Size**：对象自身占用的内存
- **Retained Size**：对象及其依赖对象的总内存（释放后可回收的空间），基本上都是看这个指标
- **Distance**：对象到 GC 根的引用层级

###### 堆快照视图

- **Summary**：按构造函数分类的内存占用

  这个就是默认的快照排列方式，根据构造函数类型按照内存占比排列

- **Comparison**：对比快照间的差异（新增/释放的对象）

  这个可以让我们非常方便的对比两个视图，有一个下拉选项可以非常方法方便的去选择和哪一个快照去做对比

  ![1753722124026](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1753722124026.png)

  其中快照有这样几列，可以清晰的对比快照中构造函数内存的变化

  - \# New：新创建的对象数量

  - \# Deleted：被删除的对象数量

  - \# Delta：净变化量（新增 - 删除）

  - Size Delta：内存大小的变化

- **Containment**：对象引用链（Retainers 视图）

   Containment 是 Chrome DevTools Memory 面板中 Heap snapshot 的一个视图模式，它展示了对象之间的引用关系和内存结构层次。

  ![1753722344181](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1753722344181.png)

  快照也有这样几列

  - Constructor：对象的构造函数名称

  - Distance：从根对象到当前对象的距离

  - Objects Count：该类型对象的数量

  - Shallow Size：对象本身占用的内存大小

  - Retained Size：对象及其所有引用对象占用的总内存大小

- **Statistics**：内存占用分布图

   Statistics 是 Chrome DevTools Memory 面板中 Heap snapshot 的一个视图模式，它提供了内存使用的统计概览，以图表和分类的方式展示内存分布情况。 

  ![1753722668840](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1753722668840.png)

##### 案例分析







##### 常见内存问题与诊断方法





##### 高级技巧与优化策略

1. **优化策略**
   - 避免频繁创建临时对象
   - 使用开发者工具的“强制GC”按钮（⚡图标）
   - 结合Performance面板分析内存与帧率的关系
2. **自动化监控方案**
   - 使用`window.performance.memory` API
   - 集成Lighthouse进行内存审计