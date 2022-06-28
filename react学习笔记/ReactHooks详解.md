##### 简介

React Hooks就是函数钩子，对函数型组件进行增强，让函数型组件可以存储状态，可以有处理副作用函数的能力，让开发者在不使用类组件的情况下实现相同的功能。这里的副作用就是不是将数据转化为视图的代码都是副作用函数，比如发送ajax，为dom绑定事件等都是副作用函数，

之所以React Hooks现在大行其道，主要是类组件有以下几个问题：

- 缺少复用机制，为了复用逻辑增加无实际渲染效果的组件，增加了组件的层级，显示十分臃肿，增加了调试的难度以及运行效率的降低
- 类组件经常变得很复杂难以维护，我们经常将一组相干的业务逻辑拆分到了多个生命周期中，在一个生命周期函数内存在多个不相干的业务逻辑
- 类成员方法不能保证this指向的正确性

Hooks就可以很好的解决上述问题，接下里先介绍下基本使用

##### 基本使用

Hooks意为钩子，React Hooks就是一堆钩子函数，React通过这些钩子函数对函数组件进行增强，不同的钩子函数提供了不同的功能。接下来简单的介绍下常见的钩子函数：

###### useState()

用于为函数组件引入状态，基本用法如下：

```javascript
function App() {
  const [count ,setCount] = useState(0);
  return (
    <div>
      <span>{count}</span>
      <button onClick={() => setCount(count + 1)}>点击</button>
    </div>
  );
}
```

这里对useState做一个总结：

- 接受唯一的参数即状态初始值，初始值可以是任意数据类型
- 返回值为数组，数组中存储状态值和更改状态值的方法，方法约定一set开头，后面加上状态名称
- 方法可以被调用多次，用以保存不同状态值
- 参数可以是一个函数，函数返回初始状态值，函数只会被调用一次，用在初始值是动态值的情况

###### useEffects()

让函数组件拥有处理副作用的能力，类似生命周期函数。可以把useEffect看着是componentDidMount、componentDidUpdate和componentWillUNmount这三个函数的组合。

- useEffect( () => {})  会在componentDidMount和componentDidUpdate执行
- useEffect( () => {},[])  会在componentDidMount执行
- useEffect( () => () => {})  会在componentWillUNmount执行

useEffect解决了这样的两个问题：

- 按照用途将代码进行分类，将一组相干的业务逻辑归置到了同一个副作用函数中，简化重复代码，是组件内部代码更加清晰。

###### useReducer()

useReducer是另一种函数组件保存状态的方式，这个函数用法和redux类似，视图触发一个action，这个action会被reducer接收，在reducer中更改state，列个小例子：

```javascript
import { useReducer } from "react";

function reducer(state,action){
  switch(action.type){
    case 'increment':
      return state + 1;
    case 'decrement':
      return state - 1;
    default:
      return state
  }
}

function Usereducer(){
  const [count,dispath] = useReducer(reducer,0);
  return <div>
    <button onClick={() => dispath({type:'increment'})}>加</button>
    <span>{count}</span>
    <button onClick={() => dispath({type:'decrement'})}>减</button>
  </div>
}

export default Usereducer
```



###### useRef()

获取DOM元素，

```javascript
const box = useRef()
<div ref={box}></div>
//打印box.current 即可获得dom实例
```

还可以用该钩子函数来保存数据，即时组件重新渲染，保存的数据依然还在，保存的数据被更改不会触发组件重新渲染。

###### useCallback()

新能优化，缓存函数，使组件重新渲染时得到相同的函数实例

```javascript
import {useState ,memo} from 'react'

function Call(){
  const [count,setCount] = useState(0);

  const resetCount = () => {
    setCount(0);
  }
  return (
    <div>
      <span>{count}</span>
      <button onClick={() => setCount(count +1)}>+1</button>
      <Foo resetCount={resetCount}></Foo>
    </div>
  )
}

const Foo = memo(function Foo(props) {
  console.log('Foo重新渲染')
  return <div>Foo组件
    <button onClick={props.resetCount}>resetCount</button>
  </div>
})

export default Call
```

上面这个例子，每次点击resetCount按钮，都会重新渲染Foo组件，然而我们只是触发了里面的一个函数，不应该重新渲染整个函数。重新渲染Foo的原因就是，在Call组件中，点击+1按钮，会更改count的值，也就会重新渲染整个Call组件，同时也就会每次生成不同的resetCount实例，而我们把改实例传递给了Foo组件，这就会导致Foo的重新渲染。

优化方法就是用useCallback方法重写我们的resetCount函数

```javascript
const resetCount = useCallback(() => setCount(0), [setCount])
```

这样只要setCount方法不会更改，resetCount永远只会是同一个实例。

###### useContext()

在跨组件层级获取数据时简化获取数据的代码 

常规的通过context跨组件传参是这样的：

```javascript
import { createContext } from "react";

const countContext = createContext();


function Context(){
  return <countContext.Provider value = {100}>
    <Foo></Foo>
  </countContext.Provider>
}

function Foo(){
  return <countContext.Consumer>
    {
      value =>{
        return <div>{value}</div>
      }
    }
  </countContext.Consumer>
}

export default Context
```

如果改用useContext，代码就大大的简化了

```javascript
function Foo(){
  const value = useContext(countContext)
  return <div>{value}</div>
}
```



###### useMemo()

useMemo的行为类似veu中的计算属性，可以检测某个值的变化，根据变化值计算新值。useMemo会缓存计算结果，如果值没有发生变化，即时组件重新渲染，也不会重新计算，此行为可以有助于避免在每个渲染上进行昂贵的计算。

```javascript
import {userMemo} from 'react'

const result = userMemo(() =>{
	return result
},[count])
```

##### 自定义Hooks

自定义Hooks是一个函数，以use开头，是标准的封装和共享逻辑的方式，其实就是逻辑和内置Hooks的组合。

接下来写一个简单的例子：

```javascript
import {useState,useEffect} from 'react'
import axios from 'axios'

function CustomHooks(){
  const [post,setPost] = useState({});
  useEffect(() => {
    axios.get('https://jsonplaceholder.typicode.com/posts/1')
      .then(res => setPost(res.data))
  },[])
  return (
    <div>
      <div>{post.title}</div>
      <div>{post.body}</div>
    </div>
  )
}

export default CustomHooks
```

这是一个简单的组件，就是获取接口拿到返回的title和body。这个发送请求的地方，如果其他地方也要用到这个逻辑，就可以封装成一个自定义的Hooks，来实现代码复用的作用：

```javascript
import {useState,useEffect} from 'react'
import axios from 'axios'

function usePost(){
  const [post,setPost] = useState({})
  useEffect(() => {
    axios.get('https://jsonplaceholder.typicode.com/posts/1')
      .then(res => setPost(res.data))
  },[])
  return [post,setPost]
}

function CustomHooks(){
  const [post] = usePost({});
  
  return (
    <div>
      <div>{post.title}</div>
      <div>{post.body}</div>
    </div>
  )
}

export default CustomHooks
```









