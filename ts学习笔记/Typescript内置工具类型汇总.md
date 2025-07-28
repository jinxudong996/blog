Typescript 提供了一些工具类型来辅助进行常见的类型转换，非常方便，本文对这些工具类型的常见用法及原理做一个汇总。

###### Partial

用于构造一个`type`下面所有属性都设置为可选的类型，这个工具会返回一个给定类型的子集。

```tsx
interface Todo {
  title: string;
  description: string;
}

type MyTodo = Partial<Todo>;
//结果
type MyTodo = {
    title?: string | undefined;
    description?: string | undefined;
}
```

如果要实现一个`MyPartial`，达到相同的功能，可以这么做

```tsx
type MyPartial<T> = {
  [P in keyof T]?: T[P];
};

interface Todo {
  title: string;
  description: string;
}

type MyTodo = MyPartial<Todo>;
```

效果和上述一样

###### Required

 用于构造一个`Type`下面的所有属性全都设置为必填的类型， 和`Partial`效果刚好相反

```tsx
interface Props {
  a?: number;
  b?: string;
  c: number;
}

type PropsType = Required<Props>;
//输出
type PropsType = {
  a: number;
  b: string;
  c: number;
}
```

要实现一个`MyRequired`，可以这么做

```tsx
type MyRequired<T> = {
  [P in keyof T]-?: T[P];
};
```

`-?` 是一个类型修饰符，用于移除属性的可选性（即从可选属性变为必选属性）

###### Readonly

 用于构造一个`Type`下面的所有属性全都设置为`只读`的类型，意味着这个类型的所有的属性全都不可以重新赋值。 

```tsx
interface Todo {
  title: string;
  description: string;
}

type todo1 = Readonly<Todo>;
//输出
type todo1 = {
  readonly title: string;
  readonly description: string;
}
```

如果要实现一个`Myreadonly`，可以这么做

```tsx
type Myreadonly<T> = {
  readonly [P in keyof T]: T[P]
}
```

###### Record

这个工具类新的API是这样：`Record<keys,type>`， 用于构造一个对象类型，它所有的key(键)都是`Keys`类型，它所有的value(值)都是`Type`类型。这个工具类型可以被用于映射一个类型的属性到另一个类型。 

```tsx
interface CatInfo {
  age: number;
  breed: string;
}

type CatName = "miffy" | "boris" | "mordred";

type cat1 = Record<CatName, CatInfo>;
//输出
type cat1 = {
  miffy: CatInfo;
  boris: CatInfo;
  mordred: CatInfo;
};
```

现在有这样一个场景，后端返回的数据中数据不确定，该如何去定义数据类型呢，比如这样

```tsx
interface CatInfo {
  age: number;
  breed: string;
}

let mimi: CatInfo = { age: 2, breed: "tabby" };

mimi.size = "20";
```

想对`CatInfo`去做一个扩展，怎么做比较好呢，可以通过索引签名来做

```tsx
interface CatInfo {
  age: number;
  breed: string;
  [kay: string]: string | number;
}
```

还可以通过和`Record<string, any>`取交叉类型

```tsx
type CatInfo = {
  age: number;
  breed: string;
} & Record<string, any>

let mimi: CatInfo = { age: 2, breed: "tabby" };

mimi.size = "20";
```

如果要实现应一个`Myrecord`，可以这样做

```tsx
type MyRecord<K extends keyof any, T> = {
  [P in K]: T
}
```

###### pick

他的`api`是这样的`pick<Type,keys>`， 用于构造一个类型，它是从`Type`类型里面挑了一些属性`Keys`(Keys是字符串字面量 或者 字符串字面量的联合类型) 

```tsx
interface Todo {
  title: string;
  description: string;
  completed: boolean;
}

type TodoPreview = Pick<Todo, "title" | "completed">;
```

要实现这个，做过[type-challenges](https://github.com/type-challenges/type-challenges)对这个应该非常熟悉，就是第一个题

```tsx
type MyPick<T, K extends keyof T> = {
  [P in K]: T[P]
}
```

###### Exclude 

他的api是这样`Exclude<UnionType,ExcludedMembers>`，用于构造一个类型，它是从`UnionType`联合类型里面排除了所有可以赋给`ExcludedMembers`的类型。 

```tsx
type T0 = Exclude<"a" | "b" | "c", "a">;
// type T0 = "b" | "c"

type T1 = Exclude<"a" | "b" | "c", "a" | "b">;
// type T1 = "c"
```

要实现的话，可以这么做

```
type MyExclude<T, U> = T extends U ? never : T
```

###### Omit

 用于构造一个类型，它是从`Type`类型里面过滤了一些属性`Keys`(Keys是字符串字面量 或者 字符串字面量的联合类型) 

```tsx
interface Todo {
  title: string;
  description: string;
  completed: boolean;
  createdAt: number;
}

type TodoPreview = Omit<Todo, "description">;
//输出
type TodoPreview = {
  title: string;
  completed: boolean;
  createdAt: number;
}
```

要实现的话，可以这么做

```tsx
type MyOmit<T, K> = MyPick<T, MyExclude<keyof T, K>>
```



###### Extract

`api`是这样`Extract<Type,Union>` 用于构造一个类型，它是从`Type`类型里面提取了所有可以赋给`Union`的类型。 

```tsx
type T0 = Extract<"a" | "b" | "c", "a" | "f">;
// type T0 = "a"
```

要实现的话可以这么做

```tsx
type MyExtract<T, U> = T extends U ? T : never;
```



###### NonNullable

 用于构造一个类型，这个类型从`Type`中排除了所有的`null`、`undefined`的类型 

```typescript
type T0 = NonNullable<string | number | undefined>;
// type T0 = string | number
```

要实现的话，可以这么做

```tsx
type MyNonNullable<T> = T extends null | undefined ? never : T;
```

###### Parameters

 用于根据所有`Type`中函数类型的参数构造一个元祖类型。 

```typescript
type T0 = Parameters<() => string>;
// type T0 = []

type T1 = Parameters<(s: string) => void>;
// type T1 = [s: string]

type T2 = Parameters<<T>(arg: T) => T>;
// type T2 = [arg: unknown]
```

要实现的话可以这么做

```tsx
type MyParameters<T extends (...args: any[]) => any> = T extends (...args: infer P) => any ? P : never;
```



###### ConstructorParmeters

 用于根据`Type`构造函数类型来构造一个元祖或数组类型，它产生一个带着所有参数类型的元组（或者返回`never`如果`Type`不是一个函数）。 

```typescript
type T0 = ConstructorParameters<ErrorConstructor>;
// type T0 = [message?: string]

type T1 = ConstructorParameters<FunctionConstructor>;
// type T1 = string[]

type T2 = ConstructorParameters<RegExpConstructor>;
// type T2 = [pattern: string | RegExp, flags?: string]

type T3 = ConstructorParameters<any>;
// type T3 = unknown[]
```

可以这么来实现这个功能

```tsx
type MyConstructorParameters<T extends abstract new (...args: any[]) => any> = 
  T extends abstract new (...args: infer P) => any ? P : never;
```



###### ReturnType

 用于构造一个含有`Type`函数的返回值的类型。 

```typescript
type T0 = ReturnType<() => string>;
// type T0 = string

type T1 = ReturnType<(s: string) => void>;
// type T1 = void

type T2 = ReturnType<<T>() => T>;
// type T2 = unknown
```

可以这么来实现这个功能

```tsx
type MyReturnType<T extends (...args: any[]) => any> = T extends (...args: any[]) => infer R ? R : never;
```

###### InstanceType

 用于构造一个由所有`Type`的构造函数的实例类型组成的类型。 

```typescript
class C {
  x = 0;
  y = 0;
}

type T0 = InstanceType<typeof C>;
// type T0 = C

type T1 = InstanceType<any>;
// type T1 = any

type T2 = InstanceType<never>;
// type T2 = never

class Person {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}
type PersonInstance = InstanceType<typeof Person>; // Person

```

手动实现的话，这么做

```tsx
type MyInstanceType<T extends abstract new (...args: any[]) => any> = 
  T extends abstract new (...args: any[]) => infer R ? R : never;

```

