##### 

> 装饰器（Decorator）是一种与类（class）相关的语法，用来注释或修改类和类方法。许多面向对象的语言都有这项功能，目前有一个[提案](https://github.com/tc39/proposal-decorators)将其引入了 ECMAScript 

装饰器是一种函数，写成`@ + 函数名`,可以放在类和类方法的定义前面。

装饰器目前浏览器与nodeJs均不支持，需要使用[@babel/plugin-proposal-decorators](https://babel.docschina.org/docs/en/next/babel-plugin-proposal-decorators/#%E9%80%9A%E8%BF%87-node-api-%E4%BD%BF%E7%94%A8)转译下。

##### 基本用法

可以用装饰器来修饰整个类

```javascript
@name
class Person {
    //
}

function name(target){
    target.age = '18'
}

console.log(Person.age)
//18
```

name就是一个装饰器，用来装饰整个Person类，为其添加上age属性，装饰器参数target就是我们要装饰的目标类。装饰器的行为也可以理解成这样：

```javascript
@decorator
class A {}

// 等同于

class A {}
A = decorator(A) || A;
```

如果要为装饰器传递更多的参数，可以在装饰器外面封装一层函数：

```javascript
@name('20')
class Person {
    //
}


function name(age){
    return function(target){
        target.age = age
    }
    
}

console.log(Person.age)
//20
```

装饰器不经可以装饰类，也可以装饰类的属性：

```javascript
class Person {
    //
    @job
    getJob() {
        console.log(this.job)
    }
}

function job(target,name,descriptor){
    target.job = 'boss'
}
p.getJob()
//'boss'
```

装饰器一共接受三个参数，第一个是类的原型对象，第二个是要装饰的属性名，第三个是改属性的描述对象。

```javascript
class Math {
  @log
  add(a, b) {
    return a + b;
  }
}

function log(target, name, descriptor) {
  var oldValue = descriptor.value;

  descriptor.value = function() {
    console.log(`Calling ${name} with`, arguments);
    return oldValue.apply(this, arguments);
  };

  return descriptor;
}

const math = new Math();

math.add(2, 4);
```

上面这个例子是可以起到日志输出的作用。

##### 应用

###### 模拟混入

可以利用装饰器实现混入模式，混入就是一个对象之中混入另外一个对象的方法。可以利用`Object.assign`方法来实现，该方法将对象的可枚举属性添加到目标方法。

```javascript
function mixins(...list) {
    return function (target) {
        Object.assign(target.prototype, ...list);
    };
}

const Foo = {
    foo() { console.log('foo') }
};

@mixins(Foo)
class MyClass { }

let obj = new MyClass();
obj.foo() // "foo"
```



###### 监控函数执行时间

我们现在有一个需求，要监控一个函数的执行时间。可以硬编码，如下：

```javascript
class Model1 {
    getData() {
        let start = new Date().valueOf()
        try {
            // 此处省略获取数据的逻辑
            return [{
                id: 1,
                name: 'Niko'
            }, {
                id: 2,
                name: 'Bellic'
            }]
        } finally {
            let end = new Date().valueOf()
            console.log(`start: ${start} end: ${end} consume: ${end - start}`)
        }
    }
}

console.log(new Model1().getData())

//start: 1640248210669 end: 1640248210669 consume: 0
//[ { id: 1, name: 'Niko' }, { id: 2, name: 'Bellic' } ]
```

这种监控代码与原代码没有任何关系，对原函数算是破坏性修改，如果不用装饰器@语法，可以在目标类外部包裹一个函数：

```javascript
class Model1 {
  getData() {
    // 此处省略获取数据的逻辑
    return [{
      id: 1,
      name: 'Niko'
    }, {
      id: 2,
      name: 'Bellic'
    }]
  }
}

function wrap(Model, key) {
  // 获取Class对应的原型
  let target = Model.prototype

  // 获取函数对应的描述符
  let descriptor = Object.getOwnPropertyDescriptor(target, key)

  // 生成新的函数，添加耗时统计逻辑
  let log = function (...arg) {
    let start = new Date().valueOf()
    try {
      return descriptor.value.apply(this, arg) // 调用之前的函数
    } finally {
      let end = new Date().valueOf()
      console.log(`start: ${start} end: ${end} consume: ${end - start}`)
    }
  }

  // 将修改后的函数重新定义到原型链上
  Object.defineProperty(target, key, {
    ...descriptor,
    value: log      // 覆盖描述重的value
  })
}

wrap(Model1, 'getData')

console.log(new Model1().getData())


//start: 1640313418991 end: 1640313418991 consume: 0
//[ { id: 1, name: 'Niko' }, { id: 2, name: 'Bellic' } ]
```



这里定义了一个wrap函数，传入目标类和目标方法，在wrap函数中重写了目标方法，将getData转换成了log方法，随后使用defineProperty方法进行覆盖，随后调用getData实际上就是调用的log方法。这就是装饰器模式。然而这种方式有点小繁琐，可以使用@语法更加简洁：

```javascript
@log('getData')
class Model1 {
  getData(id) {
    // 此处省略获取数据的逻辑
    return [{
      id: id,
      name: 'Niko'
    }, {
      id: id,
      name: 'Bellic'
    }]
  }
}

function log(key){
  return function(target){
    // 获取函数对应的描述符
    let descriptor = Object.getOwnPropertyDescriptor(target.prototype, key)
    // 生成新的函数，添加耗时统计逻辑
    let log = function (...arg) {
      let start = new Date().valueOf()
      try {
        return descriptor.value.apply(this, arg) // 调用之前的函数
      } finally {
        let end = new Date().valueOf()
        console.log(`start: ${start} end: ${end} consume: ${end - start}`)
      }
    }
    // 将修改后的函数重新定义到原型链上
    Object.defineProperty(target.prototype, key, {
      ...descriptor,
      value: log      // 覆盖描述符重的value
    })
  }
}

console.log(new Model1().getData(3))
```







