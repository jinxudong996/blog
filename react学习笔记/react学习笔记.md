##### react生命周期

react的生命周期主要分为三个阶段，挂载、更新和卸载。

- 挂载

  - constructor

    在组件挂载之前被调用，为React.Component子类实现构造函数时，首行调用super()。

  - getDerivedStateFromProps

    返回一个对象来更新state，如果返回null，则不更新任何内容。

  - render

    是class组件中唯一必须实现的方法，用于渲染dom，该方法中必须返回reactDom，常见的就是返回一个jsx对象。

    不能再该方法中使用setState方法，回导致死循环。

  - componentDidMount

    componentDidMount() 在组件挂载后 (插入DOM树后) 立即调用，componentDidMount() 是发送网络请求、启用事件监听方法的好时机，并且可以在 此钩子函数里直接调用 setState()

- 更新

  - shouldComponentUpdate

    在组件更新之前调用，可以控制组件是否进行更新， 返回true时组件更新， 返回false则不更新。

    不能再该方法中使用setState方法，回导致死循环。

  - getSnapshotBeforeUpdate 

    在最近一次的渲染输出被提交之前调用。也就是说，在 render 之后，即将对组件进行挂载时调用。 

  - componentDidUpdate

     会在更新后会被立即调用。首次渲染不会执行 

- 卸载

  - componentWillUnmount

     在组件即将被卸载或销毁时进行调用



##### react组件传参

- props
- Provider
- 



##### hooks