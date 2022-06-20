const thunkMd =  ({dispatch}) => next => action => {
  // 1. 当前这个中间件函数不关心你想执行什么样的异步操作 只关心你执行的是不是异步操作
  // 2. 如果你执行的是异步操作 你在触发action的时候 给我传递一个函数 如果执行的是同步操作 就传递action对象
  // 3. 异步操作代码要写在你传递进来的函数中
  // 4. 当前这个中间件函数在调用你传递进来的函数时 要将dispatch方法传递过去
  if (typeof action === 'function') {
    return action(dispatch)
  }
  next(action)
}

export default thunkMd