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

首先通过`Redux.createStore`创建redux实例，参数就是我们的reducer函数，reducer函数有两个参数，一个就是我们state仓库，第二个就是我们的action。通过上图，我们看到要更新视图，首先要dispatch来触发action，于是第五步、第六步就是通过点击函数来触发action，通过action去触发reducer更改我们的state仓库；仓库更改了，就需要更新视图，就需要subscribe函数出厂了，在subscribe中对视图进行更新。

这个demo还是非常简单的，使用redux来更改数据，有点杀鸡用牛刀的感觉。在一个较大的项目中，数据管理一直都是一个难点，比如在react项目中，react组件间的通信都是单向数据流的，如果涉及层级过多，传参就会很困难，使用context如果数据过多，就会变得很难维护，这个时候redux就排上了用场。由于Store独立于组件，是的数据管理同样独立于组件，这就使得数据管理变得有迹可循，后期容易维护，组件通信也容易了许多。

























