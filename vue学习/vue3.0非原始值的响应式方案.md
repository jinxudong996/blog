#####  前言

实现响应式数据其实蛮复杂的，不想前面那样单纯的拦截get/set操作，比如如何对数组进行代理，如何支持Set、WeakSet、Map、WeakMap等。接下来进一步对响应式进行学习。

##### 理解Proxy与Reflect

以前写过一篇总结[文章](https://juejin.cn/post/7031371164911943711)

使用Proxy可以创建一个代理对象，它能够实现对其他对象的代理，允许我们拦截并重新定义一个对对象的基本操作。

比如代理对象：

```javascript
const p = new Proxy(obj, {
  get() { return obj.foo },
  set(target, key, value) {
    obj[key] = value
  }
})
```

代理函数：

```javascript
const fn = (name) => {
    console.log('我是：', name)
}

const p2 = new Proxy(fn, {
    apply(target, thisArg, argArray) {
        target.call(thisArg, ...argArray)
    }
})

p2('nick')
```

这里利用apply捕获器来拿到目标对象的调用时的this，通过call来更改this 的指向，依次来拦截函数调用。

Reflect是一个全局对象，主要有以下功能：

- reflect与proxy方法一一对应
- 将对象的一些属于语言内部方法放到reflect上
- 让obejct的操作都变成函数行为

##### 代理object

我们通过proxy对属性的读取操作进行了拦截，然而属性的读取不仅仅只有访问属性，包括判断指定的属性在指定的对象或其原型链中  key in obj，还有枚举操作，for in遍历对象。接下来一一介绍下如何拦截这些读取操作。

- 访问属性

  这个就比较简单了，直接贴代码

  ```javascript
  const obj = new Proxy(data, {
    // 拦截读取操作
    get(target, key) {
      bucket.add(effect)
      // 返回属性值
      return target[key]
    },
    // 拦截设置操作
    set(target, key, newVal) {
      // 设置属性值
      target[key] = newVal
      bucket.forEach(fn => fn())
    }
  })
  ```

  

- in操作符

  使用方法：

  ```javascript
  var mycar = {make: "Honda", model: "Accord", year: 1998};
  "make" in mycar  // 返回true
  "model" in mycar // 返回true
  ```

  in操作符的运算结果是通过一个叫HasProperty的抽象方法得到的，HasProperty方法的返回值是通过内部调用方法[[HasProperty]]得到的，其对应的拦截函数叫做has，因此可以通过has拦截器实现对in操作符的代理：

  ```javascript
  let obj = {name:'nick',age:18}
  
  let p = new Proxy(obj,{
      has(target,key){
          console.log("捕获到了")
          return Reflect.has(...arguments)
      }
  })
  
  console.log('name' in p)
  ```

  

- for in  遍历

  该操作可以使用ownKeys来拦截：

  ```javascript
  let obj = {name:'nick',age:18}
  
  let p = new Proxy(obj,{
      ownKeys(target){
          console.log("捕获到了")
          return Reflect.ownKeys(target)
      }
  })
  for (let key in p){
      console.log(key,'...',obj[key])
  }
  ```

##### 代理数组

首先理解下vue2.0是如歌监听数组的变化的呢，defineProperty是根本监听不到数组的变化的：

```javascript
obj = {
    age:[1,2,3],
    name:'nick'
}

Object.defineProperty(obj,'age',{
    get(val){
        console.log('1111',val)
        return val
    }
})


console.log(obj.age)
```

这里根本打印不到get里面的内容，想要实现对数组的监听，得重写数组的方法。更改数组自身内容的有七个方法： push 、pop 、shift 、unshift 、splice 、sort 和reverse ，接下来对着七个方法进行重写：

```javascript
// 让 arrExtend 先继承 Array 本身的所有属性
const arrExtend = Object.create(Array.prototype)
const arrMethods = [
  'push',
  'pop',
  'shift',
  'unshift',
  'splice',
  'sort',
  'reverse'
]
/**
 * arrExtend 作为一个拦截对象, 对其中的方法进行重写
 */
arrMethods.forEach(method => {
  const oldMethod = Array.prototype[method]
  const newMethod = function(...args) {
    oldMethod.apply(this, args)
    console.log(`${method}方法被执行了`)
  }
  arrExtend[method] = newMethod
})

export default {
  arrExtend
}
```

这里利用 Object.create将Array原型到arrExtend变量上，接下来遍历该原型，首先拿到原型上的方法，随后对其重写，在重写的新方法中利用apply再去调用老方法，这样既不更改原逻辑，又能实现对数组方法的监听。

验证一下：

```javascript
const {arrExtend} = require('./copyArr')

let arr = [0,1,2,3,4] 

if (Array.isArray(arr)) {
    arr.__proto__ = arrExtend
    arr.push(5)
 }

 console.log(arr)
```

实际上在vue2.0中创建响应式数据是在 observer中的，在 observer中加入上述代码即可实现对数组的监听。

接来下使用proxy实现对数组的监听：

```javascript

let p = new Proxy(arr,{
    get(val,index){
        console.log('监听到了数组的改变')
        return val[index]
    },
    set(target, property, value, receiver){
        console.log('监听到了数组的改变...')
        target[property] = value
    }
})

console.log(p[0]) 
//监听到了数组的改变
//0
```

完全能实现我们想要的效果，

##### 代理Set和Map







