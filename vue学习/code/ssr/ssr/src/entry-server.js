import { createApp } from './app'

export default context => {
  const { app } = createApp()
  //服务端路由处理  数据预处理

  return app
}