#### TS学习笔记

###### 1.简介

> TypeScript 是 JavaScript 的一个超集，支持 ECMAScript 6 标准（[ES6 教程](https://www.runoob.com/w3cnote/es6-tutorial.html)）。
>
> TypeScript 由微软开发的自由和开源的编程语言。
>
> TypeScript 设计目标是开发大型应用，它可以编译成纯 JavaScript，编译出来的 JavaScript 可以运行在任何浏览器上。

安装TypeScript 可以使用npm包管理工具：

```
npm install -g typescript
tsc -v   //Version 4.4.3
```

###### 2.基础类型

TypeScript 支持与 JavaScript 几乎相同的数据类型，此外还提供了实用的枚举类型方便我们使用。

- 布尔值

  ```
  let isDone: boolean = false
  ```

- 数字

  ```javascript
  let count: number = 10
  ```

- 字符串

  ```javascript
  let name: string = "nick"
  ```

- 数组

  ```javascript
  let list: number[] = [1, 2, 3];
  
  let list: Array<number> = [1, 2, 3]; // Array<number>泛型语法
  ```

- 元组

  元组类型允许表示一个已知元素数量和类型的数组，各元素的类型不必相同。 比如，你可以定义一对值分别为 `string` 和 `number` 类型的元组。

  ```javascript
  let x: [string, number]
  x = ['hello', 10] // OK
  x = [10, 'hello'] // Error
  ```

- 枚举

   使用枚举我们可以定义一些带名字的常量。 使用枚举可以清晰地表达意图或创建一组有区别的用例。 TypeScript 支持数字的和基于字符串的枚举。 

  ```javascript
  enum Color {Red, Green, Blue}
  let c: Color = Color.Green
  ```

  枚举类型提供的一个便利是你可以由枚举的值得到它的名字。 例如，我们知道数值为 2，但是不确定它映射到 Color 里的哪个名字，我们可以查找相应的名字：

  ```javascript
  enum Color {Red = 1, Green, Blue}
  let colorName: string = Color[2]
  
  console.log(colorName)  // 显示'Green'因为上面代码里它的值是2
  ```

  可以看到上述编译过后的js代码

  ```javascript
  var Color;
  (function (Color) {
      Color[Color["Red"] = 1] = "Red";
      Color[Color["Green"] = 2] = "Green";
      Color[Color["Blue"] = 3] = "Blue";
  })(Color || (Color = {}));
  var colorName = Color[2];
  console.log(colorName); // 显示'Green'因为上面代码里它的值是2
  ```

  

- any

  有时候，我们会想要为那些在编程阶段还不清楚类型的变量指定一个类型。 这些值可能来自于动态的内容，比如来自用户输入或第三方代码库。 这种情况下，我们不希望类型检查器对这些值进行检查而是直接让它们通过编译阶段的检查。 

   在 TypeScript 中，任何类型都可以被归为 any 类型。这让 any 类型成为了类型系统的顶级类型（也被称作全局超级类型）。

  ```javascript
  let notSure: any = 4
  notSure = 'maybe a string instead'
  notSure = false // 也可以是个 boolean
  ```

  

- void

  某种程度上来说，`void` 类型像是与 `any` 类型相反，它表示没有任何类型。 当一个函数没有返回值时，你通常会见到其返回值类型是 `void`：

  ```javascript
  function warnUser(): void {
    console.log('This is my warning message')
  }
  ```

  

- null和undefined

  TypeScript 里，`undefined` 和 `null` 两者各自有自己的类型分别叫做 `undefined` 和 `null`。 和 `void` 相似，它们的本身的类型用处不是很大：

  ```javascript
  let u: undefined = undefined
  let n: null = null
  ```

  

- never

  `never` 类型表示的是那些永不存在的值的类型。 例如， `never` 类型是那些总是会抛出异常或根本就不会有返回值的函数表达式或箭头函数表达式的返回值类型； 变量也可能是 `never` 类型，当它们被永不为真的类型保护所约束时。

  `never` 类型是任何类型的子类型，也可以赋值给任何类型；然而，没有类型是 `never` 的子类型或可以赋值给`never` 类型（除了 `never` 本身之外）。 即使 `any` 也不可以赋值给 `never`。

  ```javascript
  // 返回never的函数必须存在无法达到的终点
  function error(message: string): never {
    throw new Error(message)
  }
  
  // 推断的返回值类型为never
  function fail() {
    return error("Something failed")
  }
  
  // 返回never的函数必须存在无法达到的终点
  function infiniteLoop(): never {
    while (true) {
   }
  ```

  

- object

  `object` 表示非原始类型，也就是除 `number`，`string`，`boolean`，`symbol`，`null`或`undefined` 之外的类型。

  ```javascript
  declare function create(o: object | null): void
  
  create({ prop: 0 }) // OK
  create(null) // OK
  
  create(42) // Error
  create('string') // Error
  create(false) // Error
  create(undefined) // Error
  ```



###### 3.Typescript断言

有时候你会遇到这样的情况，你会比 TypeScript 更了解某个值的详细信息。 通常这会发生在你清楚地知道一个实体具有比它现有类型更确切的类型。

通过类型断言这种方式可以告诉编译器，“相信我，我知道自己在干什么”。 类型断言好比其它语言里的类型转换，但是不进行特殊的数据检查和解构。 它没有运行时的影响，只是在编译阶段起作用。 TypeScript 会假设你，程序员，已经进行了必须的检查。

```javascript
//尖括号语法
let someValue: any = 'this is a string'

let strLength: number = (<string>someValue).length

//as语法
let someValue: any = 'this is a string'

let strLength: number = (someValue as string).length
```



###### 4.Typescript接口

TypeScript 的核心原则之一是对值所具有的结构进行类型检查。它有时被称做“鸭式辨型法”或“结构性子类型化”。 在 TypeScript 里，接口的作用就是为这些类型命名和为你的代码或第三方代码定义契约。