TypeScript有着各种非常复杂的类型计算逻辑，作为一个初学者，对这一块很是头痛，这里对此做一个总结。

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

```
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

```javascript
type MapType<T> = {
    [
        Key in keyof T 
            as `${Key & string}${Key & string}${Key & string}`
    ]: [T[Key], T[Key], T[Key]]
}
type res = MapType<{a: 1, b: 2}>;
//
type res = {
    aaa: [1, 1, 1];
    bbb: [2, 2, 2];
}

```





































