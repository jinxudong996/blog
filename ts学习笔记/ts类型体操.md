TypeScript有着各种非常复杂的类型计算逻辑，作为一个初学者，对这一块很是头痛，这里对此做一个总结。

##### 核心知识点

###### keyof 和 in

在ts中，`keyof T` 表示获取T类型中所有的属性键

```tsx
type Person = {
  name: string;
  age: number;
}
// 结果：'name' | 'age'
type result = keyof Person
```

`in`右侧通常是一个联合类型，可以使用`in`来迭代这个联合类型

```tsx
// 仅演示使用, K为每次迭代的项
K in 'name' | 'age' | 'sex'
K = 'name' // 第一次迭代结果
K = 'age'  // 第二次迭代结果
K = 'sex'  // 第三次迭代结果
```

比如可以写一些辅助工具，比如`Readonly`

```tsx
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};
type Person = {
  name: string;
  age: number;
};
// 结果：{ readony name: string; readonly age: number; }
type result = Readonly<Person>;
```

这里的` [P in keyof T] `就是遍历T中的每一个属性键，并且赋值为P，相当于`for in`

###### typeof

 `TS`中的`typeof`，可以用来获取一个`JavaScript`变量的类型，经常用于获取一个普通对象或者一个函数的类型， 比如

```tsx
const obj = {
  name: 'AAA',
  age: 23
}
type t2 = typeof obj
```



###### extends

 `extends`关键词，一般有两种用法：**类型约束**和**条件类型**。 

类型约束经常和泛型一起使用，

比如` U extends keyof T `，就表明U是T属性键中的一种

条件类型和常见的三元表达式一样，

```tsx
type isTwo<T> = T extends 2 ? true: false;
```

###### infer

 `infer`关键词的作用是延时推导，它会在类型未推导时进行占位，等到真正推导成功后，它能准确的返回正确的类型。 

提取元组类型中的第一个元素：

```tsx
type First<Tuple extends unknown[]> = Tuple extends [infer T,...infer R] ? T : never;
```

还有这个，提取函数返回类型的工具

```tsx
type ReturnType<T> = T extends (...args: any) => infer R ? R : never

const add = (a: number, b: number): number => {
  return a + b
}
// 结果: number
type result = ReturnType<typeof add>
```

- `T extends (...args: any) => infer R`：如果不看`infer R`，这段代码实际表示：`T`是不是一个函数类型。
- `(...args: any) => infer R`：这段代码实际表示一个函数类型，其中把它的参数使用`args`来表示，把它的返回类型用`R`来进行占位。 如果`T`满足是一个函数类型，那么我们返回其函数的返回类型，也就是`R`；如果不是一个函数类型，就返回`never`。

##### 模式匹配

###### 数组类型

数组类型想要获取第一个元素，可以这样写：

```javascript
type GetFirst<arr extends unknown[]> = arr extends [infer F ,...unknown[]] ? F :never;
```

测试一下：

```javascript
type GetFirstResult = GetFirst<['123',2,3]>  //'123'
```

这里用的`unknown`它和`any`的都是可以表示任意类型，而`any`还可以赋值给任意类型。

如果想要获取最后一个类型参数的话，也比较简单：

```javascript
type GetLast<arr extends unknown[]> = arr extends [...unknown[],infer F] ? F :never;

type GetLastResult = GetLast<['123',2,{}]>
```

如果想要获取最后一个参数之外的剩余数组元素，可以这样写：

```javascript
type PopArr<Arr> = 
    Arr extends [] ? [] 
        : Arr extends [...infer Rest,unknown] ? Rest : never;

type getPopArr = PopArr<['123321',{},1,2,3,4,'123']> //'123321',{},1,2,3,4,
```

这里的unknown就相当于占位置，通过这个可以获取到除去元素的剩余元素等。

###### 字符串类型

也可以通过匹配模式来判断字符串是否以某个前缀开头：

```javascript
type StartsWith<Str extends string, Prefix extends string> = 
    Str extends `${Prefix}${string}` ? true : false;

type StartsWithResult = StartsWith<'aabbcc','aa'> //true
```

做字符串替换：

```javascript
type ReplaceStr<
    Str extends string,
    From extends string,
    To extends string
> = Str extends `${infer Prefix}${From}${infer Suffix}` 
        ? `${Prefix}${To}${Suffix}` : Str;
```

去除空格：

```javascript
type TrimStrRight<Str extends string> = 
    Str extends `${infer Rest}${' ' | '\n' | '\t'}` 
        ? TrimStrRight<Rest> : Str;
```

###### 函数类型

函数类型可以通过模式匹配来获取参数的类型：

```javascript
type GetParameters<Func extends Function> = Func extends (...args: infer Args) => unknown ? Args : never;

type GetParametersResult = GetParameters<(name:'nick') => string>
```

通过模式匹配获取返回值的类型：

```javascript
type GetReturnType<Func extends Function> = 
    Func extends (...args: any[]) => infer ReturnType 
        ? ReturnType : never;

type GetReturnTypeResult = GetReturnType<() => {name:'nick'}>
```

##### 重新构造

TypeScript的type、infer、类型参数申明的变量都不能修改，想要产生新的类型就需要用重新构造。

###### 数组类型

向数组末尾添加新的类型：

```javascript
type Push<Arr extends unknown[], Ele> = [...Arr, Ele];
type PUSHResult = Push<[1,2,3],{name:'nick'}>
```

或者是向数组前面添加新的类型：

```tsx
type Push<Arr extends unknown[], Ele> = [Ele,...Arr];
type PUSHResult = Push<[1,2,3],{name:'nick'}>
```

如果是合并两个数组，可以这样做：

```javascript
type tuple1 = [1,2];
type tuple2 = ['guang', 'dong'];
```



```javascript
type Zip<One extends [unknown, unknown], Other extends [unknown, unknown]> = 
    One extends [infer OneFirst, infer OneSecond]
        ? Other extends [infer OtherFirst, infer OtherSecond]
            ? [[OneFirst, OtherFirst], [OneSecond, OtherSecond]] :[] 
                : [];
```



###### 字符串类型

可以将字符串首字母转化为大写：

```javascript
type CapitalizeStr<Str extends string> = 
    Str extends `${infer First}${infer Rest}` 
        ? `${Uppercase<First>}${Rest}` : Str;
```

字符串下划线转化为驼峰：

```javascript
type CamelCase<Str extends string> = 
    Str extends `${infer Left}_${infer Right}${infer Rest}`
        ? `${Left}${Uppercase<Right>}${CamelCase<Rest>}`
        : Str;
```

删除指定字符串：

```javascript
type DropSubStr<Str extends string, SubStr extends string> = 
    Str extends `${infer Prefix}${SubStr}${infer Suffix}` 
        ? DropSubStr<`${Prefix}${Suffix}`, SubStr> : Str;
```

###### 函数类型

在已有的函数类型上添加一个参数：

```javascript
type AppendArgument<Func extends Function, Arg> = 
    Func extends (...args: infer Args) => infer ReturnType 
        ? (...args: [...Args, Arg]) => ReturnType : never;
```

###### 映射类型

对象、class在TypeScript对应的类型就是索引类型，对索引类型做修改，就要用到映射类型。

接下来对索引类型的值进行更改：

```javascript
type MapType<T> = {
    [Key in keyof T]: [T[Key], T[Key], T[Key]]
}

type res = MapType<{a: 1, b: 2}>;
//
type res = {
    a: [1, 1, 1];
    b: [2, 2, 2];
}
```

对索引类型的索引进行更改：

```tsx
type MapType<T> = {
  [Key in keyof T as `${Key & string}${Key & string}${Key & string}`]: [
    T[Key],
    T[Key],
    T[Key]
  ];
};
type res = MapType<{ a: 1; b: 2 }>;
```



##### 递归复用

递归就是将问题分解为相似的一系列小问题，通过函数调用自身来解决这些问题，直到满足结束条件。TypeScript类型系统不支持循环，当处理数量的个数、长度、层级不确定时，就可以通过递归来处理。

###### 数组类型

反转一个数组，比如` type arr = [1,2,3,4,5]; `，可以这样写：

```javascript
type ReverseArr<Arr extends unknown[]> = 
    Arr extends [infer First, ...infer Rest] 
        ? [...ReverseArr<Rest>, First] 
        : Arr; 

type ReverseArrResult = ReverseArr<[1,2,3,4,5]> //[5.4.3.2.1]
```

也可以用于查找元素，比如在一个数组` type arr = [1,2,3,4,5]; `中查找等于5，有就返回true，没有就返回false。

```javascript
type Includes<Arr extends unknown[], FindItem> = 
    Arr extends [infer First, ...infer Rest]
        ? IsEqual<First, FindItem> extends true
            ? true
            : Includes<Rest, FindItem>
        : false;

type IsEqual<A, B> = (A extends B ? true : false) & (B extends A ? true : false);
type IncludesResult = Includes<[1,2,3,4,5],5> //true
```

删除指定元素：

```javascript
type RemoveItem<
    Arr extends unknown[], 
    Item, 
    Result extends unknown[] = []
> = Arr extends [infer First, ...infer Rest]
        ? IsEqual<First, Item> extends true
            ? RemoveItem<Rest, Item, Result>
            : RemoveItem<Rest, Item, [...Result, First]>
        : Result;
        
type IsEqual<A, B> = (A extends B ? true : false) & (B extends A ? true : false);
```

###### 字符串类型

字符串替换：

```javascript
type ReplaceAll<
    Str extends string, 
    From extends string, 
    To extends string
> = Str extends `${infer Left}${From}${infer Right}`
        ? `${Left}${To}${ReplaceAll<Right, From, To>}`
        : Str;
```

字符串反转：

```javascript
type ReverseStr<
    Str extends string, 
    Result extends string = ''
> = Str extends `${infer First}${infer Rest}` 
    ? ReverseStr<Rest, `${First}${Result}`> 
    : Result;
```

###### 对象类型

 对象类型的递归，也可以叫做索引类型的递归。 

` readonly  `是一个内置的工具类型，如果要实现的话可以这么做：

```tsx
type ToReadonly<T> =  {
    readonly [Key in keyof T]: T[Key];
}
```

如果对象的嵌套层级不确定，就需要用到递归了

```tsx
type DeepReadonly<Obj extends Record<string, any>> = {
    readonly [Key in keyof Obj]:
        Obj[Key] extends object
            ? Obj[Key] extends Function
                ? Obj[Key] 
                : DeepReadonly<Obj[Key]>
            : Obj[Key]
}
```

如果是 object 类型并且还是 Function，那么就直接取之前的值 Obj[Key]。

如果是 object 类型但不是 Function，那就是说也是一个索引类型，就递归处理 DeepReadonly<Obj[Key]>。

##### 数值运算

 TypeScript 类型系统中没有加减乘除运算符，但是可以通过构造不同的数组然后取 length 的方式来完成数值计算，把数值的加减乘除转化为对数组的提取和构造。

###### 加减乘除

1. ###### 加法

```tsx
type BuildArray<
  Length extends number,
  Ele = unknown,
  Arr extends unknown[] = []
> = Arr["length"] extends Length ? Arr : BuildArray<Length, Ele, [...Arr, Ele]>;

type Add<Num1 extends number, Num2 extends number> = [
  ...BuildArray<Num1>,
  ...BuildArray<Num2>
]["length"];

type result = Add<50, 50>; //100
```

这里首先定义了一个`BuildArray`，其中类型参数 Length 是要构造的数组的长度。类型参数 Ele 是数组元素，默认为 unknown。类型参数 Arr 为构造出的数组，默认是 []。 因为数组长度不确定，这里用到了递归， 如果 Arr 的长度到达了 Length，就返回构造出的 Arr，否则继续递归构造。 

这里的`Add`就很简单了，应用了下`BuildArray`然后返回数组的`[length]`。

2. ###### 减法

   减法这里的思路就是模式提取，比如 3 是 [unknown, unknown, unknown] 的数组类型，提取出 2 个元素之后，剩下的数组再取 length 就是 1。 确实有点奇技淫巧的感觉。

   ```tsx
   type Subtract<
     Num1 extends number,
     Num2 extends number
   > = BuildArray<Num1> extends [...arr1: BuildArray<Num2>, ...arr2: infer Rest]
     ? Rest["length"]
     : never;
   type subResult = Subtract<100, 50>; //50
   ```

3. ###### 乘法

   乘法就是多个加法的累加

   ```tsx
   type Mutiply<
     Num1 extends number,
     Num2 extends number,
     ResultArr extends unknown[] = []
   > = Num2 extends 0
     ? ResultArr["length"]
     : Mutiply<Num1, Subtract<Num2, 1>, [...BuildArray<Num1>, ...ResultArr]>;
   
   type MulResult = Mutiply<10, 10>; //10
          
   ```

   类型参数 Num1 和 Num2 分别是被加数和加数。

   因为乘法是多个加法结果的累加，我们加了一个类型参数 ResultArr 来保存中间结果，默认值是 []，相当于从 0 开始加。

   每加一次就把 Num2 减一，直到 Num2 为 0，就代表加完了。

   加的过程就是往 ResultArr 数组中放 Num1 个元素。

   这样递归的进行累加，也就是递归的往 ResultArr 中放元素。

   最后取 ResultArr 的 length 就是乘法的结果。

4. ###### 除法

    除法实际上就是递归的累减 

   ```tsx
   type Divide<
     Num1 extends number,
     Num2 extends number,
     CountArr extends unknown[] = []
   > = Num1 extends 0
     ? CountArr["length"]
     : Divide<Subtract<Num1, Num2>, Num2, [unknown, ...CountArr]>;
   
   type DivResult = Divide<100, 10>; //10
   ```

   类型参数 Num1 和 Num2 分别是被减数和减数。

   类型参数 CountArr 是用来记录减了几次的累加数组。

   如果 Num1 减到了 0 ，那么这时候减了几次就是除法结果，也就是 CountArr['length']。

   否则继续递归的减，让 Num1 减去 Num2，并且 CountArr 多加一个元素代表又减了一次。



##### 联合类型

当类型参数为联合类型，并且在条件类型左边直接引用该类型参数的时候，TypeScript 会把每一个元素单独传入来做类型运算，最后再合并成联合类型，这种语法叫做分布式条件类型。

定义一个联合类型` type Union = 'a' | 'b' | 'c'; `

让这个联合类型其中的`a`大写，可以这么做

```tsx
type Union = "a" | "b" | "c";
type UppercaseA<Item extends string> = Item extends "a"
  ? Uppercase<Item>
  : Item;
type Result = UppercaseA<Union>;
```

 这里就不需要递归提取每个元素再处理 



































