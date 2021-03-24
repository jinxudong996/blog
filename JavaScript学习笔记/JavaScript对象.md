#### JavaScript对象

> 对象就是一组属性的无序集合

###### 属性

> 属性分为数据属性和访问器属性

数据属性主要有四个特性

- Configurable    表示属性是否可以通过delete删除并重新定义，是否可以修改它的特性，以及是否可以把它改为访问器属性。默认为true
- Enumerable  表示属性是否可以通过for-in循环返回。默认为true
- Writable  表示属性的值是否可以被修改。默认为true
- Value  包含属性实际的值。默认为undefined

修改属性的默认特性，得使用Object.defineProperty()，该方法接收三个参数：要给其添加属性的对象、属性的名称和描述符对象。

```JavaScript
let person = {}
Object.defineProperty(person, 'name', {
    writable: false,
    value: 'nick'
})
console.log(person.name)  // nick
person.name = 'tom'
console.log(person.name)  // nick
```

访问器属性也有四个特性描述他们的行为：

- configured  表示属性是否可以通过delete删除并重新定义，是否可以修改它的特性，以及是否可以把它改为访问器属性。默认为true
- Enumerable  表示属性是否可以通过for-in循环返回。默认为true
- get  获取函数，在读取属性值时调用，默认为undefined
- set   设置函数，在写入属性时调用，默认为undefined

访问器属性也要通过Object.defineProperty()函数来修改。

```JavaScript
let book = {
    year_: 2021,
    edition: 1
}
Object.defineProperty(book, 'year', {
    get(val) {
        console.log('getting', val)
        return this.year_
    },
    set(val) {
        console.log('setting---',val)
        //this.year_ = val
        this.edition += 1
    }
})
book.year = 2050   // setting--- 20250
console.log(book.year_)  //2021
console.log(book.year)  // getting undefined  2021 
console.log(book.edition  2
```

加入需要在同一个对象上定义多个属性，则需要使用Object.defineProperties()方法，该方法接收两个参数，要修改的对象和描述符对象，用法同Object.defineProperty()一致。vue的v-model双向绑定就是利用Object.defineProperty()方法的get与set方法来实现的。



Object.assign()，该方法接收一个目标对象和一个或多个源对象作为参数，将每个源对象中可枚举属性（）和自有属性复制到目标对象上。该方法的原理就是，对每个符合条件的属性，调用源对象上的get方法取得属性值，使用目标对象的set方法设置属性值。该方法只是浅复制。



> 对象解构：使用对象匹配的结构来完成复制

```javascript
let person = {
    name: 'nick',
    age: 18
}
let { name, age} = person  //解构赋值
let {name, job} = person //如果没匹配到，就是undefined
let {name, job='singer'} = person  //设置默认值
```

