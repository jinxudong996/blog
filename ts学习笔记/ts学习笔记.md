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

```javascript
interface LabelledValue {
  label: string
}

function printLabel(labelledObj: LabelledValue) {
  console.log(labelledObj.label)
}

let myObj = {size: 10, label: 'Size 10 Object'}
printLabel(myObj)
```

运行 `tsc interface.js`  可以看待编译后的js代码：

```javascript
function printLabel(labelledObj) {
    console.log(labelledObj.label);
}
var myObj = { size: 10, label1: 'Size 10 Object' };
printLabel(myObj);
```

`LabelledValue` 接口就好比一个名字，用来描述上面例子里的结构。 它代表了有一个 `label` 属性且类型为`string` 的对象。 需要注意的是，我们在这里并不能像在其它语言里一样，说传给 `printLabel` 的对象实现了这个接口。我们只会去关注值的外形。 只要传入的对象满足上面提到的必要条件，那么它就是被允许的。

还有一点值得提的是，类型检查器不会去检查属性的顺序，只要相应的属性存在并且类型也是对的就可以。



###### 4.1  可选属性

接口里的属性不全都是必需的。 有些是只在某些条件下存在，或者根本不存在。例如给函数传入的参数对象中只有部分属性赋值了。

```javascript
interface Square {
  color: string,
  area: number
}

interface SquareConfig {
  color?: string
  width?: number
}

function createSquare (config: SquareConfig): Square {
  let newSquare = {color: 'white', area: 100}
  if (config.color) {
    newSquare.color = config.color
  }
  if (config.width) {
    newSquare.area = config.width * config.width
  }
  return newSquare
}

let mySquare = createSquare({color: 'black'})
```

运行 `tsc interface2.js`  可以看待编译后的js代码：

```javascript
function createSquare(config) {
    var newSquare = { color: 'white', area: 100 };
    if (config.color) {
        newSquare.color = config.color;
    }
    if (config.width) {
        newSquare.area = config.width * config.width;
    }
    return newSquare;
}
var mySquare = createSquare({ color: 'black' });
console.log(mySquare)
```

带有可选属性的接口与普通的接口定义差不多，只是在可选属性名字定义的后面加一个 `?` 符号。

可选属性的好处之一是可以对可能存在的属性进行预定义，好处之二是可以捕获引用了不存在的属性时的错误。

###### 4.2 只读属性

属性名前用 `readonly` 来指定只读属性:

```javascript
interface Point {
  readonly x: number
  readonly y: number
}

let p1: Point = { x: 10, y: 20 }
// p1.x = 5 // error!
```

######    4.3额外的属性检查

```javascript
interface SquareConfig {
    color?: string;
    width?: number;
}

function createSquare (config: SquareConfig): { color: string; area: number } {
  let newSquare = {color: 'white', area: 100}
  if (config.color) {
    newSquare.color = config.color
  }
  if (config.width) {
    newSquare.area = config.width * config.width
  }
  return newSquare
}


let mySquare = createSquare({ colour: 'red', width: 100 })
```

注意传入 `createSquare` 的参数拼写为 `colour` 而不是 `color`。 在 JavaScript 里，这会默默地失败。可以使用类型断言来绕过检查：

```javascript
let mySquare = createSquare({ width: 100, opacity: 0.5 } as SquareConfig)
```

或者使用赋值来绕过：

```javascript
let squareOptions = { colour: 'red', width: 100 }
let mySquare = createSquare(squareOptions)
```

最好的方式是使用索引签名：

```javascript
interface SquareConfig {
  color?: string
  width?: number
  [propName: string]: any
}
```

表示的是`SquareConfig` 可以有任意数量的属性，并且只要它们不是 `color` 和 `width`，那么就无所谓它们的类型是什么。

######    4.4函数类型

给接口定义一个调用签名。它就像是一个只有参数列表和返回值类型的函数定义。参数列表里的每个参数都需要名字和类型。

```javascript
interface SearchFunc {
  (source: string, subString: string): boolean
}

let mySearch: SearchFunc
mySearch = function(source: string, subString: string): boolean {
  let result = source.search(subString);
  return result > -1
}
```

编译后的代码：

```javascript
var mySearch;
mySearch = function (source, subString) {
    var result = source.search(subString);
    return result > -1;
};
```

对于函数类型的类型检查来说，函数的参数名不需要与接口里定义的名字相匹配。 比如，我们使用下面的代码重写上面的例子：

```typescript
let mySearch: SearchFunc
mySearch = function(src: string, sub: string): boolean {
  let result = src.search(sub);
  return result > -1
}
```

函数的参数会逐个进行检查，要求对应位置上的参数类型是兼容的。 如果你不想指定类型，TypeScript 的类型系统会推断出参数类型，因为函数直接赋值给了  `SearchFunc` 类型变量。 函数的返回值类型是通过其返回值推断出来的（此例是 `false` 和 `true`）。 如果让这个函数返回数字或字符串，类型检查器会警告我们函数的返回值类型与 `SearchFunc` 接口中的定义不匹配。

```typescript
let mySearch: SearchFunc
mySearch = function(src, sub) {
  let result = src.search(sub)
  return result > -1
}
```

######   4.5 可索引的类型

与使用接口描述函数类型差不多，我们也可以描述那些能够“通过索引得到”的类型，比如 `a[10]` 或 `ageMap['daniel']`。 可索引类型具有一个 索引签名，它描述了对象索引的类型，还有相应的索引返回值类型。

```javascript
interface StringArray {
  [index: number]: string
}

let myArray: StringArray
myArray = ['Bob', 'Fred']

let myStr: string = myArray[0]
```

我们定义了 `StringArray` 接口，它具有索引签名。 这个索引签名表示了当用 `number` 去索引 `StringArray` 时会得到 `string` 类型的返回值。编译后的代码为：

```javascript
var myArray;
myArray = ['Bob', 'Fred'];
var myStr = myArray[0];
```

TypeScript 支持两种索引签名：字符串和数字。 可以同时使用两种类型的索引，但是数字索引的返回值必须是字符串索引返回值类型的子类型。 这是因为当使用 `number` 来索引时，JavaScript 会将它转换成`string` 然后再去索引对象。 也就是说用 `100`（一个 `number`）去索引等同于使用`'100'`（一个 `string` ）去索引，因此两者需要保持一致。

```typescript
class Animal {
  name: string
}
class Dog extends Animal {
  breed: string
}

// 错误：使用数值型的字符串索引，有时会得到完全不同的Animal!
interface NotOkay {
  [x: number]: Animal
  [x: string]: Dog
}
```

字符串索引签名能够很好的描述 `dictionary` 模式，并且它们也会确保所有属性与其返回值类型相匹配。 因为字符串索引声明了 `obj.property` 和 `obj['property']` 两种形式都可以。 下面的例子里， `name` 的类型与字符串索引类型不匹配，所以类型检查器给出一个错误提示：

```typescript
interface NumberDictionary {
  [index: string]: number;
  length: number;    // 可以，length是number类型
  name: string       // 错误，`name`的类型与索引类型返回值的类型不匹配
}
```

最后，你可以将索引签名设置为只读，这样就防止了给索引赋值：

```typescript
interface ReadonlyStringArray {
  readonly [index: number]: string;
}
let myArray: ReadonlyStringArray = ['Alice', 'Bob'];
myArray[2] = 'Mallory'; // error!
```

######  5.类类型

###### 5.1 实现接口

与 C# 或 Java 里接口的基本作用一样，TypeScript 也能够用它来明确的强制一个类去符合某种契约。

```typescript
interface ClockInterface {
  currentTime: Date
}

class Clock implements ClockInterface {
  currentTime: Date
  constructor(h: number, m: number) { }
}
```

你也可以在接口中描述一个方法，在类里实现它，如同下面的 `setTime` 方法一样：

```typescript
interface ClockInterface {
  currentTime: Date
  setTime(d: Date)
}

class Clock implements ClockInterface {
  currentTime: Date
  setTime(d: Date) {
    this.currentTime = d
  }
  constructor(h: number, m: number) { }
}
```

接口描述了类的公共部分，而不是公共和私有两部分。 它不会帮你检查类是否具有某些私有成员。

