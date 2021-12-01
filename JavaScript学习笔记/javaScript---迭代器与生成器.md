##### 迭代概念

> 循环是迭代机制的基础，这是因为它可以指定迭代的次数，以及每次迭代要执行什么操作。每次循 环都会在下一次迭代开始之前完成，而每次迭代的顺序都是事先定义好的。  

> 在 JavaScript 中，**迭代器**是一个对象，它定义一个序列，并在终止时可能返回一个返回值。 更具体地说，迭代器是通过使用 `next()` 方法实现 [Iterator protocol](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols#The_iterator_protocol) 的任何一个对象，该方法返回具有两个属性的对象： `value`，这是序列中的 next 值；和 `done` ，如果已经迭代到序列中的最后一个值，则它为 `true` 。如果 `value` 和 `done` 一起存在，则它是迭代器的返回值。
>
> 一旦创建，迭代器对象可以通过重复调用next（）显式地迭代。 迭代一个迭代器被称为消耗了这个迭代器，因为它通常只能执行一次。 在产生终止值之后，对next（）的额外调用应该继续返回{done：true}。

> 它是一种接口，为各种不同的数据结构提供统一的访问机制。任何数据结构只要部署 Iterator 接口，就可以完成遍历操作（即依次处理该数据结构的所有成员） 

Iterator 的作用有三个：一是为各种数据结构，提供一个统一的、简便的访问接口；二是使得数据结构的成员能够按某种次序排列；三是 ES6 创造了一种新的遍历命令`for...of`循环 。

其遍历过程是这样的：

- 创建一个指针对象，指向当前数据结构的起始位置。也就是说，遍历器对象本质上，就是一个指针对象
-  第一次调用指针对象的`next`方法，可以将指针指向数据结构的第一个成员
-  第二次调用指针对象的`next`方法，指针就指向数据结构的第二个成员 
-  不断调用指针对象的`next`方法，直到它指向数据结构的结束位置 

每一次调用`next`方法，都会返回数据结构的当前成员的信息。具体来说，就是返回一个包含`value`和`done`两个属性的对象。其中，`value`属性是当前成员的值，`done`属性是一个布尔值，表示遍历是否结束。 



##### Iterator 接口 

Iterator 接口的目的，就是为所有数据结构，提供了一种统一的访问机制，即`for...of`循环 。

一种数据结构只要部署了 Iterator 接口，我们就称这种数据结构是“可遍历的” 。

terator 接口部署在数据结构的`Symbol.iterator`属性，或者说，一个数据结构只要具有`Symbol.iterator`属性，就可以认为是“可遍历的”（iterable）。`Symbol.iterator`属性本身是一个函数，就是当前数据结构默认的遍历器生成函数。执行这个函数，就会返回一个遍历器。 

原生具备 Iterator 接口的数据结构如下：

- Array
- Map
- Set
- String
- TypedArray
- 函数的 arguments 对象
- NodeList 对象

创建一个迭代器：

```javascript
function createIterator(items) {
    var i = 0;
    return {
        next: function() {
            var done = i >= item.length;
            var value = !done ? items[i++] : undefined;

            return {
                done: done,
                value: value
            };
        }
    };
}

// iterator 就是一个迭代器对象
var iterator = createIterator([1, 2, 3]);

console.log(iterator.next()); // { done: false, value: 1 }
console.log(iterator.next()); // { done: false, value: 2 }
console.log(iterator.next()); // { done: false, value: 3 }
console.log(iterator.next()); // { done: true, value: undefined }
```

然后这并不是一个真正的迭代器，使用`for of`遍历会报错`iterator is not iterable`，因为`iterator`并没有设置` Symbol.iterator `属性，更改下

```javascript
iterator[Symbol.iterator] = function() {
    return createIterator([1, 2, 3]);
};

for (value of iterator) {
    console.log(value);
}
```

或者直接给一个对象添加` Symbol.iterator `

```javascript
const obj = {
    value: 1
};

obj[Symbol.iterator] = function() {
    return createIterator([1, 2, 3]);
};

for (value of obj) {
    console.log(value);
}
```

