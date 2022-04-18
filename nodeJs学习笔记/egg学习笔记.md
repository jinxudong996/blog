##### controller

添加一个user路由：

在controller路径下添加一个`user.js`

```javascript
'use strict';

const Controller = require('egg').Controller;

class UserController extends Controller{
  async index(){
    const {ctx} = this;

    ctx.body = 'user index'
  }

  async lists(){
    const {ctx} = this;
    await new Promise(resolve => {
      setTimeout(() => {
        resolve()
      }, 500);
    })
    ctx.body = 'hello user/lists'
  }
}

module.exports = UserController
```

注册controller需要在`route.js`中添加：

```javascript
router.get('/user', controller.user.index);
router.get('/user/lists', controller.user.lists);
```

这里注册了一个index方法和lists方法，index方法就是简单的向ctx的body中写入一个字符串，lists方法模拟了一个异步方法，等待0.5s后向页面输出hello user/lists



##### get请求处理

获取get请求后面的参数，需要使用`ctx.query`

```javascript
async detail(){
    const { ctx } = this;
    ctx.body = ctx.query;
}
```

如果要获取动态的id，比如这样的路由：

```
router.get('/user/detail2/:id', controller.user.detail2);
```

就需要使用`ctx.params`:

```javascript
async detail2(){
    const { ctx } = this;
    ctx.body = ctx.query;
}
```



##### post请求处理

```javascript
async add() {
  const { ctx } = this;
  ctx.body = {
    status: 200,
    data: ctx.request.body,
  };
}
```

换可以使用`egg-validate`插件来约束传入参数，在`config/plugin.js`中配置：

```javascript
exports.validate = {
  enable: true,
  package: 'egg-validate',
};
```







##### Service处理