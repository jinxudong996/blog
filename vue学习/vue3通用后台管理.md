前端要努力

仿照 [vue-element-admin](https://panjiachen.github.io/vue-element-admin-site/zh/) 做一个通用版的管理后台，基于vue3和elementui涵盖国际化、权限验证、动态路由等管理后台常见的方案，还有一些管理后台常见的业务中的一些换肤、全屏和动态表格渲染等。

后端服务目前依托于第三方，后续打算使用nest自己开发一套。处于暂定中。

#### 框架搭建

首先来完成登录页面

##### 登录

首先完成登录的ui处理。在`src/view/login.vue`写入登录样式

```html
<el-form class="login-form" :model="loginForm" :rules="loginRules" ref="loginFromRef">
  <div class="title-container">
    <h3 class="title">{{ $t('msg.login.title') }}</h3>
  </div>

  <el-form-item prop="username">
    <span class="svg-container">
      <svg-icon icon="user" />
    </span>
    <el-input
      placeholder="username"
      name="username"
      type="text"
      v-model="loginForm.username"
    />
  </el-form-item>

  <el-form-item prop="password">
    <span class="svg-container">
      <svg-icon icon="password" />
    </span>
    <el-input
      placeholder="password"
      name="password"
      v-model="loginForm.password"
      :type="passwordType"
    />
    <span class="show-pwd">
      <svg-icon
        :icon="passwordType === 'password' ? 'eye' : 'eye-open'"
        @click="onChangePwdType"
      />
    </span>
  </el-form-item>

  <el-button
    type="primary"
    style="width: 100%; margin-bottom: 30px"
    :loading="loading"
    @click="handleLogin"
    >{{ $t('msg.login.loginBtn') }}</el-button
  >
</el-form>
```

这里样式比较简单，就两个输入框，用户名和密码，随后就是一个点击登录的按钮。

###### 输入校验及密码处理

其中未输入框添加了输入校验， 这里的表单校验同`element-ui` 一样，校验规则是这样的

```js
// 验证规则
const loginRules = ref({
  username: [
    {
      required: true,
      trigger: 'blur',
      message: '用户名为必填项'
    }
  ],
  password: [
    {
      required: true,
      trigger: 'blur',
      validator: validatePassword()
    }
  ]
})

//密码校验规则
export const validatePassword = () => {
  return (rule, value, callback) => {
    if (value.length < 6) {
      callback(new Error(i18n.global.t('msg.login.passwordRule')))
    } else {
      callback()
    }
  }
}
```

这里用户名做了必输校验，而密码通过使用自定义的校验函数，添加了密码长度的校验，而`i18n`这里暂时先略过，是后续的做国际化所用到点。

上述密码框还做了密码状态的切换，通过点击小眼睛来切换密码的明文和密文，这里也比较简单

```js
// 处理密码框文本显示状态
const passwordType = ref('password')
const onChangePwdType = () => {
  if (passwordType.value === 'password') {
    passwordType.value = 'text'
  } else {
    passwordType.value = 'password'
  }
}
```

通过定义一个`passwordType`变量，来更改`el-input`的type值，切换明文和密文，而眼睛的变化通过自定义组件`svg-icon`传入不同的icon来实现。

###### 登录操作

当我们输入完用户名和密码，点击登录按钮后，通常会做如下处理

1. 使用封装的axios向后端发起请求，获取请求数据
2. 拿到请求数据后，存储用户信息及token
3. 登录鉴权

其中用户信息后续在页面内进行一些展示，比如用户手机号、用户id等，后续都会用到，而token也是非常关键的，后续所有的请求都会带上这个token。而登录鉴权就是用户未登录时只能进入登录页，登录后在token过期之前不允许进入登录页。

接下来首先封装axios

###### 请求封装

新建文件`src/utils/request.js`

```javascript
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 5000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 在这个位置需要统一的去注入token
    if (store.getters.token) {
      if (isCheckTimeout()) {
        // 登出操作
        store.dispatch('user/logout')
        return Promise.reject(new Error('token 失效'))
      }
      // 如果token存在 注入token
      config.headers.Authorization = `Bearer ${store.getters.token}`
    }
    // 配置接口国际化
    config.headers['Accept-Language'] = store.getters.language
    return config // 必须返回配置
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const { success, message, data } = response.data
    //   要根据success的成功与否决定下面的操作
    if (success) {
      return data
    } else {
      // 业务错误
      ElMessage.error(message) // 提示错误消息
      return Promise.reject(new Error(message))
    }
  },
  error => {
    // 处理 token 超时问题
    if (
      error.response &&
      error.response.data &&
      error.response.data.code === 401
    ) {
      // token超时
      store.dispatch('user/logout')
    }
    ElMessage.error(error.message) // 提示错误信息
    return Promise.reject(error)
  }
)

export default service
```

首先在根目录下定义一些[环境变量](https://cli.vuejs.org/zh/guide/mode-and-env.html)

```
.env.development
# 标志
ENV = 'development'

# base api
VUE_APP_BASE_API = '/api'

.env.production
# 标志
ENV = 'production'

# base api
VUE_APP_BASE_API = '/prod-api'
```

这是通过vue-cli脚手架创建项目可以通过这种方式来定义环境变量，通过`process.env`来获取。

首先创建一个service实例，这里就用到了刚刚创建的环境变量，通过`process.env.VUE_APP_BASE_API`来定义`baseURL`，紧接着定义了请求拦截器和响应拦截器。

在请求拦截器中，首先判断`store.getters.token`是否有token，如果有在判断是否过期，过期的话就直接做登出操作，未过期就直接在`headers`中注入token。后面还在`headers`中注入了`Accept-Language`字段，表明当前语言的环境，后续接口国际化处理。

这里判断过期的操作是通过对比时间来做的，**后续处理**

在响应拦截中做了下错误的区分，是接口错误还是业务错误，接口错误就是常见的404，以及5开头的服务器错误，这是通常是服务端出现了异常，通过弹框提示，比如这里通过状态码异常，来处理token过期的问题；业务错误是指接口正常响应了，通常接口的入参出现了问题，这里也暂时做弹窗处理，实际可以根据业务做一些具体的区分。

###### 装请求模块

请求封装了，还要封装请求模块，比如登录接口

新建文件`src/api/sys.js`

```js
import request from '@/utils/request'

/**
 * 登录
 */
export const login = data => {
  return request({
    url: '/sys/login',
    method: 'POST',
    data
  })
}
```

###### 封装登录请求动作

该动作我们期望把它封装到 `vuex` 的 `action` 中

对于vuex的用法，看下[官网](https://vuex.vuejs.org/)的一张[图](https://vuex.vuejs.org/vuex.png)我觉得就够了。state是我们的核心仓库，所有的数据都放在这里，要改变这个数据要使用 `Mutation` 来通过commit来触发，如果涉及到异步的操作了，就要通过在`action`里定义异步方法commit一个`Mutation` 来更改数据，而触发action的方法就是通过dispatch来触发。在实际项目中，更多的通过`namespaced: true`使用模块的方式定义vuex，这样好处就是可以隔离变量。

新建文件`src/store/modules/user.js`

```js
export default {
  namespaced: true,
  state: () => ({
    token: getItem(TOKEN) || '',
    userInfo: {}
  }),
  mutations: {
    setToken(state, token) {
      state.token = token
      setItem(TOKEN, token)
    },
    setUserInfo(state, userInfo) {
      state.userInfo = userInfo
    }
  },
  actions: {
    login(context, userInfo) {
      const { username, password } = userInfo
      return new Promise((resolve, reject) => {
        login({
          username,
          password: md5(password)
        })
          .then(data => {
            this.commit('user/setToken', data.token)
            // 保存登录时间
            setTimeStamp()
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    async getUserInfo(context) {
      const res = await getUserInfo()
      this.commit('user/setUserInfo', res)
      return res
    },
    logout() {
      resetRouter()
      this.commit('user/setToken', '')
      this.commit('user/setUserInfo', {})
      removeAllItem()
      router.push('/login')
    }
  }
}

```

在state中定义了token和userInfo对象，在mutations中定义了setToken和setUserInfo方法，在action中定义了登录login方法、获取信息的getUserInfo和登出的logout方法。

这里的login方法就是刚刚封装的请求模块，传入username和加密后的password，然后将返回值中的token保存到state中，同时调用setTimeStamp方法，这个方法就是将当前登录的时间戳定义在localStorage中，也是前面前端计算token过期的一个方法。

###### 触发登录

在按钮上绑定点击事件

```js
// 登录动作处理
const loading = ref(false)
const loginFromRef = ref(null)
const store = useStore()
const router = useRouter()
const handleLogin = () => {
  loginFromRef.value.validate(valid => {
    if (!valid) return

    loading.value = true
    store
      .dispatch('user/login', loginForm.value)
      .then(() => {
        loading.value = false
        // 登录后操作
        router.push('/')
      })
      .catch(err => {
        console.log(err)
        loading.value = false
      })
  })
}
```

这里就是表单校验通过后，通过dispatch触发action，完成登录请求。成功后直接跳转首页。

###### 登录鉴权

完成登录鉴权，需要用到[路由守卫](https://router.vuejs.org/zh/guide/advanced/navigation-guards.html#%E5%85%A8%E5%B1%80%E5%89%8D%E7%BD%AE%E5%AE%88%E5%8D%AB)。

创建文件`permission.js`

```js
// 白名单
const whiteList = ['/login']
/**
 * 路由前置守卫
 */
router.beforeEach(async (to, from, next) => {
  // 存在 token ，进入主页
  // 快捷访问
  if (store.getters.token) {
    if (to.path === '/login') {
      next('/')
    } else {
      // 判断用户资料是否获取
      // 若不存在用户信息，则需要获取用户信息
      if (!store.getters.hasUserInfo) {
        // 触发获取用户信息的 action，并获取用户当前权限
        const { permission } = await store.dispatch('user/getUserInfo')
        // 处理用户权限，筛选出需要添加的权限
        const filterRoutes = await store.dispatch(
          'permission/filterRoutes',
          permission.menus
        )
        console.log(filterRoutes)
        // 利用 addRoute 循环添加
        filterRoutes.forEach(item => {
          router.addRoute(item)
        })
        // 添加完动态路由之后，需要在进行一次主动跳转
        return next(to.path)
      }
      next()
    }
  } else {
    // 没有token的情况下，可以进入白名单
    if (whiteList.indexOf(to.path) > -1) {
      next()
    } else {
      next('/login')
    }
  }
})
```

这里实际上也比较简单，就是每次路由跳转都会检查下是否有token，如果有在检查下如果目标路由是登录页的话就直接跳转到首页，如果目标路由不是登录页的话，检查下是否获取了用户信息，没有的话就再次请求下重新获取，然后**处理下权限**；如果没有token，在根据具体情况是否直接跳转到登录页。

##### layout

###### 基本ui





###### 退出登录





###### 动态menu





###### 面包屑





###### 菜单



###### 面包屑



##### 常见业务梳理



###### 国际化



###### 换肤



###### 全屏



###### 头部搜索



###### tagsview



###### 引导页



