##### state

组件能够通过props接收外部的数据，还可以拥有自己的状态state，此状态在组件内部可以被更新，状态更新也会导致dom更新。组件内部的状态数据被存储在state属性中，state属性值为对象类型，属性名称固定不可更改。react中组件有两种：类组件和函数组件，接下来一一总结下：

###### 类组件

类组件中通过`setState`方法更新组件

```javascript
setState(obj,callback)
```

- 第一个参数obj，如果是对象，则是即将合并的state；如果是一个函数，会将当前组件的state和props作为参数，返回值用于合并新的state。
- 第二个参数callback，callback函数在执行上下文中可以拿到当前setState更新后的state值，可以在此做一些基于dom的操作

当一个setState函数执行时，会发生什么事情呢，或者说一个完整的setState流程是啥呢：

- 首先，setState 会产生当前更新的优先级（老版本用 expirationTime ，新版本用 lane ）。

- 接下来 React 会从 fiber Root 根部 fiber 向下调和子节点，调和阶段将对比发生更新的地方，更新对比 expirationTime ，找到发生更新的组件，合并 state，然后触发 render 函数，得到新的 UI 视图层，完成 render 阶段。

- 接下来到 commit 阶段，commit 阶段，替换真实 DOM ，完成此次更新流程。

- 此时仍然在 commit 阶段，会执行 setState 中 callback 函数,如上的`()=>{ console.log(this.state.number) }`，到此为止完成了一次 setState 全过程。

  这里蛮多不懂的，包括state合并的优先级、批量更新等等。。。慢慢搞，加油。

###### 函数组件

react-hooks使得函数组件可以和类组件一样拥有state，可以通过useState来更改ui视图，其用法如下：

```javascript
[state, dispatch ] = useState(initData)
```

- state渲染视图的数据

- dispatch，改变state的函数，也就是推动函数组件渲染的渲染函数，

  这里dispatch的参数有两种情况，一是新的值赋值给state，作为下一次渲染使用，还可以当做一个函数返回新的state

- initDta，可以是state的值，也可以是返回state值的函数

###### 监听state的变化

- 类组件

  在类组件中， 有第二个参数callback 或者是生命周期componentDidUpdate 可以检测监听到 state 改变或是组件更新 

- 函数组件

   通常可以把 state 作为依赖项传入 useEffect 第二个参数 deps 

##### props

对于在React应用中的子组件，无论是函数组件还是类组件，父组件绑定在标签里的属性和方法，都会通过props传递给他们。















