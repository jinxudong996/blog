##### redux核心

###### 简介

redux是一个`JavaScript`状态容器，提供可预测化的状态管理。

![](https://raw.githubusercontent.com/jinxudong996/blog/main/images/redux.jpg)

redux主要有四个核心概念

- Store 存储状态的容器，JavaScript对象
- View  视图，html页面
- Action 对象，描述对状态进行怎样的操作
- Reducers 函数，操作并返回新的状态

接下来通过redux实现一个简单的计数器，加深对redux的认识：

```html
<button id="plus">+</button>
<span id="count">0</span>
<button id="minus">-</button>
```

```javascript
// 3. 存储默认状态
var initialState = {
  count: 0
}
// 2. 创建 reducer 函数
function reducer (state = initialState, action) {
  switch (action.type) {
    case 'increment':
      return {count: state.count + 1};
    case 'decrement':
      return {count: state.count - 1}
    default:
      return state;
  }
}
// 1. 创建 store 对象
var store = Redux.createStore(reducer);

// 4. 定义 action
var increment = { type: 'increment' };
var decrement = { type: 'decrement' };

// 5. 获取按钮 给按钮添加点击事件
document.getElementById('plus').onclick = function () {
  // 6. 触发action
  store.dispatch(increment);
}

document.getElementById('minus').onclick = function () {
  // 6. 触发action
  store.dispatch(decrement);
}

// 7. 订阅 store
store.subscribe(() => {
  // 获取store对象中存储的状态
  // console.log(store.getState());
  document.getElementById('count').innerHTML = store.getState().count;
})
```

首先通过`Redux.createStore`创建redux实例，参数就是我们的reducer函数，reducer函数有两个参数，一个就是我们state仓库，第二个就是我们的action。通过上图，我们看到要更新视图，首先要dispatch来触发action，于是第五步、第六步就是通过点击函数来触发action，通过action去触发reducer更改我们的state仓库；仓库更改了，就需要更新视图，就需要subscribe函数出场了，在subscribe中对视图进行更新。

这个demo还是非常简单的，使用redux来更改数据，有点杀鸡用牛刀的感觉。在一个较大的项目中，数据管理一直都是一个难点，比如在react项目中，react组件间的通信都是单向数据流的，如果涉及层级过多，传参就会很困难，使用context如果数据过多，就会变得很难维护，这个时候redux就排上了用场。由于Store独立于组件，是的数据管理同样独立于组件，这就使得数据管理变得有迹可循，后期容易维护，组件通信也容易了许多。



##### react+redux

上面为了了解redux，流程图画的较为的简单，接下来再重新介绍下redux工作流程

![](https://raw.githubusercontent.com/jinxudong996/blog/main/images/react-redux.png)

- 组件通过dispatch方法触发action
- Store接受action并将Action分发给Reducer
- Reducer根据Action类型对状态进行更改并将更改后的状态返回给Store
- 组件订阅了Store中的状态，Store中的状态更新会同步到组件中

接下来使用react来重构上述的计数器

```javascript
//index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
// import App from './App';

import {createStore} from 'redux';

const initialState = {
  count:0
}

function reducer(state = initialState,action){
  switch (action.type) {
    case 'increment':
      return {count: state.count + 1};
    case 'decrement':
      return {count: state.count - 1}
    default:
      return state;
  }
}

const store = createStore(reducer)

const increment = {type:'increment'}
const decrement = {type:'decrement'}

function Counter(){
  return (
    <div>
      <button onClick={() => store.dispatch(increment)}>+</button>
      <span>{store.getState().count}</span>
      <button onClick={() => store.dispatch(decrement)}>-</button>
    </div>
  )
}

store.subscribe(() => {
  root.render(
    <Counter/>
  );
})

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Counter/>
);


```

这种写法实际上有个很大的问题，平常我们封装的组件都是在一个文件夹里单独导入的，在单独的组件内如何拿到Store实例，以及触发subscribe函数，这就需要一个插件`react-redux`出场了。这个插件中主要暴露了一个组件和一个方法，Provider组件和contect方法。

- Provider组件，这个组件将我们的Store实例放到全局作用域上，让所有的组件都能够引用，使用方法如下：

  ```javascript
  <Provider store={store}>
     <Counter/>
  </Provider>
  //需要包裹项目的所有的组件
  ```

- contect方法主要有以下几个功能

  - 会订阅store，当store中的状态发生更改时，会重新渲染组件
  - 可以获取store中的状态，将状态通过组件的props属性映射给组件
  - 可以获取dispatch方法





















