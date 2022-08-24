type GetFirst<arr extends unknown[]> = arr extends [infer F ,...unknown[]] ? F :never;

type GetFirst1<Arr extends unknown[]> = 
    Arr extends [infer First, ...unknown[]] ? First : never;

type GetLast<arr extends unknown[]> = arr extends [...unknown[],infer F] ? F :never;

type GetLastResult = GetLast<['123',2,{}]>

type PopArr<Arr> = 
    Arr extends [] ? [] 
        : Arr extends [...infer Rest,unknown] ? Rest : never;

type getPopArr = PopArr<['123321',{},1,2,3,4,'123']>


type StartsWith<Str extends string, Prefix extends string> = 
    Str extends `${Prefix}${string}` ? true : false;

type StartsWithResult = StartsWith<'aabbcc','aa'>

type ReplaceStr<
    Str extends string,
    From extends string,
    To extends string
> = Str extends `${infer Prefix}${From}${infer Suffix}` 
        ? `${Prefix}${To}${Suffix}` : Str;

type GetParameters<Func extends Function> = Func extends (...args: infer Args) => unknown ? Args : never;

type GetParametersResult = GetParameters<(name:'nick') => string>

type GetReturnType<Func extends Function> = 
    Func extends (...args: any[]) => infer ReturnType 
        ? ReturnType : never;

type GetReturnTypeResult = GetReturnType<() => {name:'nick'}>


type tuple = [1,2,3];

type Push<Arr extends unknown[], Ele> = [...Arr, Ele];
type PUSHResult = Push<[1,2,3],{name:'nick'}>


// type MapType<T> = {
//   [Key in keyof T]: [T[Key], T[Key], T[Key]]
// }

// type res = MapType<{a: 1, b: 2}>;

type MapType<T> = {
  [
      Key in keyof T 
          as `${Key & string}${Key & string}${Key & string}`
  ]: [T[Key], T[Key], T[Key]]
}
type res = MapType<{a: 1, b: 2}>;
