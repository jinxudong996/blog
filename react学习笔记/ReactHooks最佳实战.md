##### 简介

React Hooks就是函数钩子，对函数型组件进行增强，让函数型组件可以存储状态，可以有处理副作用函数的能力，让开发者在不使用类组件的情况下实现相同的功能。这里的副作用就是不是将数据转化为视图的代码都是副作用函数，比如发送ajax，为dom绑定事件等都是副作用函数，

之所以React Hooks现在大行其道，主要是类组件有以下几个问题：

- 缺少复用机制，为了复用逻辑增加无实际渲染效果的组件，增加了组件的层级，显示十分臃肿，增加了调试的难度以及运行效率的降低
- 类组件经常变得很复杂难以维护，我们经常将一组相干的业务逻辑拆分到了多个生命周期中，在一个生命周期函数内存在多个不相干的业务逻辑
- 类成员方法不能保证this指向的正确性

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





###### useCallback()



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













