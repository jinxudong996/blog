前端要努力

仿照 [vue-element-admin](https://panjiachen.github.io/vue-element-admin-site/zh/) 做一个通用版的管理后台，基于vue3和elementui涵盖国际化、权限验证、动态路由等管理后台常见的方案，还有一些管理后台常见的业务中的一些换肤、全屏和动态表格渲染等。

后端服务目前依托于第三方，后续打算使用nest自己开发一套。

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

这里判断过期的操作是通过对比登录时间来做的，定义在`utils/auth`的一个工具方法

```js
export function isCheckTimeout() {
  // 当前时间戳
  var currentTime = Date.now()
  // 缓存时间戳
  var timeStamp = getTimeStamp()
  return currentTime - timeStamp > TOKEN_TIMEOUT_VALUE
}
```

`getTimeStamp`就是获取登录时存储的时间戳，然后和当前时间戳来做一个差值，超过2小时就算是超时了。

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

layout实际上就是常见的管理后台的布局，左侧是菜单，右侧分为上下两块，上面是NavBar，下面就是Content部分了。如下面代码：

```js
<template>
  <div class="app-wrapper">
    <!-- 左侧 menu -->
    <sidebar
      id="guide-sidebar"
      class="sidebar-container"
    />
    <div class="main-container">
      <div class="fixed-header">
        <!-- 顶部的 navbar -->
        <navbar />
      </div>
      <!-- 内容区 -->
      <app-main />
    </div>
  </div>
</template>
```



###### 退出登录

对于退出登录而言，触发时机一般有两种：

1. 主动退出，指的是用户主动点击退出按钮
2. 被动退出，指的是token过期或者账户被其他人登录

当我们推出登录时，需要处理这些事情：

1. 清理掉当前用户缓存数据
2. 清理掉权限相关配置
3. 返回到登录页

接下来首先处理下主动退出：

同样将行为封装在vuex中，就是在登录时定义的 `store/modules/user.js`

```js
import router from '@/router'

logout() {
    this.commit('user/setToken', '')
    this.commit('user/setUserInfo', {})
    removeAllItem()
    router.push('/login')
}
```

然后绑定下点击事件即可

```js
const logout = () => {
  store.dispatch('user/logout')
}
```

关于token失效，通常都会在服务端进行处理，而这里在前端也进行了处理，算是双保险吧。在前面登录鉴权和封装axios时已经做好了。而账户被其他人登录，这个需要服务端进行处理，这里一般会约定返回指定的状态码。

###### 动态menu

在后台管理中都会涉及到权限管理，不同权限的人看到的菜单都会不一样。比较简单的实现动态菜单的方式就是后端根据用户权限返回一个树，前端遍历这个树来生成菜单，路由的话就直接指定全量路由，但是这种有一个问题，就是用户根据链接来访问他没有权限的路由实际上也是可以的，不够严谨。比较好的方式就是结合动态路由表来实现。

首先将路由表分为`publicRoutes`和`privateRoutes`，其中`publicRoutes`是不需要权限就能进入的公开路由表，比如登录页，404等；而`privateRoutes`是需要权限才能进入的全量私有路由表，在注册时，只注册公开路由表，私有路由表根据权限匹配动态添加。

注册路由代码：

```js
const router = createRouter({
  history:
    process.env.NODE_ENV === 'production'
      ? createWebHistory()
      : createWebHashHistory(),
  routes: publicRoutes
})

export default router
```

定义全量的私有路由代码：

```js
export const privateRoutes = [
  UserManageRouter,
  RoleListRouter,
  PermissionListRouter,
  ArticleRouter,
  ArticleCreaterRouter
]
```

如何拿到当前用户的权限呢，这里一般都是后端会返回的，比如当前这个项目返回的权限就在用户信息中，数据时这样的

```json
{
    "menus": [
        "userManage",
        "roleList",
        "permissionList",
        "articleRanking",
        "articleCreate"
    ],
    "points": [
        "distributeRole",
        "importUser",
        "removeUser",
        "distributePermission"
    ]
}
```

在前面的登录鉴权，定义在一个全局的路由守卫中，每次路由跳转都会触发

```js
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
```

其中的`permission`就是权限数组，`dispatch`触发的`action`是这样写的

```js
filterRoutes(context, menus) {
      const routes = []
      // 路由权限匹配
      menus.forEach(key => {
        // 权限名 与 路由的 name 匹配
        routes.push(...privateRoutes.filter(item => item.name === key))
      })
      // 最后添加 不匹配路由进入 404
      routes.push({
        path: '/:catchAll(.*)',
        redirect: '/404'
      })
      context.commit('setRoutes', routes)
      return routes
    }
```

遍历下传入的权限数组，然后从私有路由表匹配出路由，通过`addRoute`添加到路由中。

这样复合用户当前权限的路由就生成了，然后就可以通过这个路由表的数据来动态生成菜单了。

`SidebarMenu.vue`

```vue
<el-menu
    :default-active="activeMenu"
    :collapse="!$store.getters.sidebarOpened"
    :background-color="$store.getters.cssVar.menuBg"
    :text-color="$store.getters.cssVar.menuText"
    :active-text-color="$store.getters.cssVar.menuActiveText"
    :unique-opened="true"
    router
  >
    <sidebar-item
      v-for="item in routes"
      :key="item.path"
      :route="item"
    ></sidebar-item>
  </el-menu>
```

`SidebarItem.vue`

```vue
<!-- 支持渲染多级 menu 菜单 -->
<el-sub-menu v-if="route.children.length > 0" :index="route.path">
    <template #title>
<menu-item :title="route.meta.title" :icon="route.meta.icon"></menu-item>
    </template>
    <!-- 循环渲染 -->
    <sidebar-item
                  v-for="item in route.children"
                  :key="item.path"
                  :route="item"
                  ></sidebar-item>
</el-sub-menu>
<!-- 渲染 item 项 -->
<el-menu-item v-else :index="route.path">
    <menu-item :title="route.meta.title" :icon="route.meta.icon"></menu-item>
</el-menu-item>

```

`MenuItem.vue`

```vue
<template>
  <i v-if="icon.includes('el-icon')" class="sub-el-icon" :class="icon"></i>
  <svg-icon v-else :icon="icon"></svg-icon>
  <span>{{ generateTitle(title) }}</span>
</template>
```

上面就是我们的动态菜单了，其中`routes`是通过`router.getRoutes()`获得数据经过格式化处理得来的。



###### 动态面包屑

动态面包屑就是根据当前的 `url` 自动生成面包屑导航菜单

```vue

  <el-breadcrumb class="breadcrumb" separator="/">
    <transition-group name="breadcrumb">
      <el-breadcrumb-item
        v-for="(item, index) in breadcrumbData"
        :key="item.path"
      >
        <!-- 不可点击项 -->
        <span v-if="index === breadcrumbData.length - 1" class="no-redirect">{{
          generateTitle(item.meta.title)
        }}</span>
        <!-- 可点击项 -->
        <a v-else class="redirect" @click.prevent="onLinkClick(item)">{{
          generateTitle(item.meta.title)
        }}</a>
      </el-breadcrumb-item>
    </transition-group>
  </el-breadcrumb>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
// 生成数组数据
const breadcrumbData = ref([])
const getBreadcrumbData = () => {
  breadcrumbData.value = route.matched.filter(
    item => item.meta && item.meta.title
  )
}
// 监听路由变化时触发
watch(
  route,
  () => {
    getBreadcrumbData()
  },
  {
    immediate: true
  }
)
</script>

```



##### 常见业务梳理

###### 国际化

国际化就是根据业务需要来实现网站的语言切换，目前社区已经有了成熟的第三方库 [vue-i18n](https://vue-i18n.intlify.dev/) 。

首先对`i18n`进行实例化

```js
import { createI18n } from 'vue-i18n'
import mZhLocale from './lang/zh'
import mEnLocale from './lang/en'
import store from '@/store'

const messages = {
  en: {
    msg: {
      ...mEnLocale
    }
  },
  zh: {
    msg: {
      ...mZhLocale
    }
  }
}

/**
 * 返回当前 lang
 */
function getLanguage() {
  return store && store.getters && store.getters.language
}
const i18n = createI18n({
  // 使用 Composition API 模式，则需要将其设置为false
  legacy: false,
  // 全局注入 $t 函数
  globalInjection: true,
  locale: getLanguage(),
  messages
})

export default i18n

```

`mZhLocale`和`mEnLocale`使我们准备的文本，两个相同key不同value的JSON文件，然后在`main.js`中进行注册

```js
import i18n from '@/i18n'

installIcons(app)
```

接下来定义存储相关变量的仓库

```js
import { LANG } from '@/constant'
import { getItem, setItem } from '@/utils/storage'
export default {
  namespaced: true,
  state: () => ({
    ...
    language: getItem(LANG) || 'zh'
  }),
  mutations: {
    ...
    /**
     * 设置国际化
     */
    setLanguage(state, lang) {
      setItem(LANG, lang)
      state.language = lang
    }
  },
  actions: {}
}

```

用vuex来存储变量，然后写一个切换语言的组件

```js
<template>
  <el-dropdown
    trigger="click"
    class="international"
    @command="handleSetLanguage"
  >
    <div>
      <el-tooltip :content="$t('msg.navBar.lang')" :effect="effect">
        <svg-icon id="guide-lang" icon="language" />
      </el-tooltip>
    </div>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item :disabled="language === 'zh'" command="zh">
          中文
        </el-dropdown-item>
        <el-dropdown-item :disabled="language === 'en'" command="en">
          English
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { defineProps, computed } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

defineProps({
  effect: {
    type: String,
    default: 'dark',
    validator: function(value) {
      // 这个值必须匹配下列字符串中的一个
      return ['dark', 'light'].indexOf(value) !== -1
    }
  }
})

const store = useStore()
const language = computed(() => store.getters.language)

// 切换语言的方法
const i18n = useI18n()
const handleSetLanguage = lang => {
  i18n.locale.value = lang
  store.commit('app/setLanguage', lang)
  ElMessage.success(i18n.t('msg.toast.switchLangSuccess'))
}
</script>

```

然后再业务代码中这样使用

```vue
 <h3 class="title">{{ $t('msg.login.title') }}</h3>
```

`title`就是我们定义的JSON文件中的key。

这里对我们的内部组件就完成了国际化，根据切换`language`就可以完成语言的切换，

这里只是对页面上展示的文本，还记得前面的动态菜单嘛，哪里的数据就是从后端返回的，这就需要接口也实现国际化，即根据制定变量返回制定的语言，实际上我们在封装请求的请求拦截器中已经完成了：

```js
config.headers['Accept-Language'] = store.getters.language
```

在请求头中加上一个`Accept-Language`，剩下的就交给后端处理了。







###### 换肤

换肤其实是一个不怎么常见的需求，相对于管理平台来说，如果是一个新项目比较好做，如果是维护一个老项目，要加上换肤操作，那就很是麻烦了。

接下来看一下换肤具体是怎么做的。

在画页面时，涉及到颜色的不要写死，通过变量来动态控制

```scss
// sidebar
$menuText: #bfcbd9;
$menuActiveText: #ffffff;
$subMenuActiveText: #f4f4f5;

$menuBg: #304156;
$menuHover: #263445;

$subMenuBg: #1f2d3d;
$subMenuHover: #001528;

$sideBarWidth: 210px;
$hideSideBarWidth: 54px;
$sideBarDuration: 0.28s;

// https://www.bluematador.com/blog/how-to-share-variables-between-js-and-sass
// JS 与 scss 共享变量，在 scss 中通过 :export 进行导出，在 js 中可通过 ESM 进行导入
:export {
  menuText: $menuText;
  menuActiveText: $menuActiveText;
  subMenuActiveText: $subMenuActiveText;
  menuBg: $menuBg;
  menuHover: $menuHover;
  subMenuBg: $subMenuBg;
  subMenuHover: $subMenuHover;
  sideBarWidth: $sideBarWidth;
}

```

然后通过变量来动态的改变这个颜色就可以了，还是比较简单的，当天这是针对自定义组件，对于第三方组件库的换肤，还是有点麻烦的。需要有以下三步：

1. 获取当前 `element-plus` 的所有样式
2. 找到我们想要替换的样式部分，通过正则完成替换
3. 把替换后的样式写入到 `style` 标签中，利用样式优先级的特性，替代固有样式



首先新建一个颜色转换器

```json
{
  "shade-1": "color(primary shade(10%))",
  "light-1": "color(primary tint(10%))",
  "light-2": "color(primary tint(20%))",
  "light-3": "color(primary tint(30%))",
  "light-4": "color(primary tint(40%))",
  "light-5": "color(primary tint(50%))",
  "light-6": "color(primary tint(60%))",
  "light-7": "color(primary tint(70%))",
  "light-8": "color(primary tint(80%))",
  "light-9": "color(primary tint(90%))",
  "subMenuHover": "color(primary tint(70%))",
  "subMenuBg": "color(primary tint(80%))",
  "menuHover": "color(primary tint(90%))",
  "menuBg": "color(primary)"
}

```

就是以`primary`为基准，来添加shade(10%)的黑色，tint(10%)的白色，tint(20%)的白色等。

```js
import color from 'css-color-function'
import rgbHex from 'rgb-hex'
import formula from '@/constant/formula.json'
import axios from 'axios'

/**
 * 根据主色值，生成最新的样式表
 */
export const generateNewStyle = async primaryColor => {
  const colors = generateColors(primaryColor)
  let cssText = await getOriginalStyle()

  // 遍历生成的样式表，在 CSS 的原样式中进行全局替换
  Object.keys(colors).forEach(key => {
    cssText = cssText.replace(
      new RegExp('(:|\\s+)' + key, 'g'),
      '$1' + colors[key]
    )
  })

  return cssText
}

/**
 * 根据主色生成色值表
 */
export const generateColors = primary => {
  if (!primary) return
  const colors = {
    primary
  }
  Object.keys(formula).forEach(key => {
    const value = formula[key].replace(/primary/g, primary)
    colors[key] = '#' + rgbHex(color.convert(value))
  })
  return colors
}

/**
 * 获取当前 element-plus 的默认样式表
 */
const getOriginalStyle = async () => {
  const version = require('element-plus/package.json').version
  const url = `https://unpkg.com/element-plus@${version}/dist/index.css`
  const { data } = await axios(url)
  // 把获取到的数据筛选为原样式模板
  return getStyleTemplate(data)
}

/**
 * 返回 style 的 template
 */
const getStyleTemplate = data => {
  // element-plus 默认色值
  const colorMap = {
    '#3a8ee6': 'shade-1',
    '#409eff': 'primary',
    '#53a8ff': 'light-1',
    '#66b1ff': 'light-2',
    '#79bbff': 'light-3',
    '#8cc5ff': 'light-4',
    '#a0cfff': 'light-5',
    '#b3d8ff': 'light-6',
    '#c6e2ff': 'light-7',
    '#d9ecff': 'light-8',
    '#ecf5ff': 'light-9'
  }
  // 根据默认色值为要替换的色值打上标记
  Object.keys(colorMap).forEach(key => {
    const value = colorMap[key]
    data = data.replace(new RegExp(key, 'ig'), value)
  })
  return data
}

```

首先根据主色生成色值表，就是根据上面的颜色转换器来实现的。然后获取到element-plus 的默认样式表，给所有需要替换的颜色打上标记，打标记就是为了待会替换颜色所用；打标记所用的模板就是`colorMap`，就`getStyleTemplate`方法，然后再遍历色值表进行替换就行了。

写一个方法将新生成的css样式写入到`head`标签里就行了，

```js
export const writeNewStyle = elNewStyle => {
  const style = document.createElement('style')
  style.innerText = elNewStyle
  document.head.appendChild(style)
}
```

###### 全屏

对于 `screenfull ` 而言，浏览器本身已经提供了对用的 [API](https://developer.mozilla.org/zh-CN/docs/Web/API/Fullscreen_API)，这个 `API` 中，主要提供了两个方法：

1. [`Document.exitFullscreen()`](https://developer.mozilla.org/zh-CN/docs/Web/API/Document/exitFullscreen)：该方法用于请求从全屏模式切换到窗口模式
2. [`Element.requestFullscreen()`](https://developer.mozilla.org/zh-CN/docs/Web/API/Element/requestFullScreen)：该方法用于请求浏览器（user agent）将特定元素（甚至延伸到它的后代元素）置为全屏模式
   1. 比如我们可以通过 `document.getElementById('app').requestFullscreen()` 在获取 `id=app` 的 `DOM` 之后，把该区域置为全屏

但是该方法存在一定的小问题，比如：

1. `appmain` 区域背景颜色为黑色

所以通常情况下我们不会直接使用该 `API` 来去实现全屏效果，而是会使用它的包装库 [screenfull](https://www.npmjs.com/package/screenfull)

```VUE
<template>
  <div>
    <svg-icon
      :icon="isFullscreen ? 'exit-fullscreen' : 'fullscreen'"
      @click="onToggle"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import screenfull from 'screenfull'

// 是否全屏
const isFullscreen = ref(false)

// 监听变化
const change = () => {
  isFullscreen.value = screenfull.isFullscreen
}

// 切换事件
const onToggle = () => {
  screenfull.toggle()
}

// 设置侦听器
onMounted(() => {
  screenfull.on('change', change)
})

// 删除侦听器
onUnmounted(() => {
  screenfull.off('change', change)
})
</script>

<style lang="scss" scoped></style>

```

###### 头部搜索

`headerSearch` 是复杂后台系统中非常常见的一个功能，在指定搜索框中对当前应用中所有页面进行检索，以 `select` 的形式展示出被检索的页面，以达到快速进入的目的

这里其实拆分下需求，就是一个搜索框，根据输入的内容，检索数据源，显示一个`select`然后点击可以跳转路由就行了。数据源就是我们左侧的动态的动态菜单。

```vue
<template>
  <div :class="{ show: isShow }" class="header-search">
    <svg-icon
      id="guide-search"
      class-name="search-icon"
      icon="search"
      @click.stop="onShowClick"
    />
    <el-select
      ref="headerSearchSelectRef"
      class="header-search-select"
      v-model="search"
      filterable
      default-first-option
      remote
      placeholder="Search"
      :remote-method="querySearch"
      @change="onSelectChange"
    >
      <el-option
        v-for="option in searchOptions"
        :key="option.item.path"
        :label="option.item.title.join(' > ')"
        :value="option.item"
      ></el-option>
    </el-select>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { generateRoutes } from './FuseData'
import Fuse from 'fuse.js'
import { filterRouters } from '@/utils/route'
import { useRouter } from 'vue-router'
import { watchSwitchLang } from '@/utils/i18n'

// 控制 search 显示
const isShow = ref(false)
// el-select 实例
const headerSearchSelectRef = ref(null)
const onShowClick = () => {
  isShow.value = !isShow.value
  headerSearchSelectRef.value.focus()
}

// search 相关
const search = ref('')
// 搜索结果
const searchOptions = ref([])
// 搜索方法
const querySearch = query => {
  if (query !== '') {
    searchOptions.value = fuse.search(query)
  } else {
    searchOptions.value = []
  }
}
// 选中回调
const onSelectChange = val => {
  router.push(val.path)
  onClose()
}

// 检索数据源
const router = useRouter()
let searchPool = computed(() => {
  const filterRoutes = filterRouters(router.getRoutes())
  return generateRoutes(filterRoutes)
})
/**
 * 搜索库相关
 */
let fuse
const initFuse = searchPool => {
  fuse = new Fuse(searchPool, {
    // 是否按优先级进行排序
    shouldSort: true,
    // 匹配算法放弃的时机， 阈值 0.0 需要完美匹配（字母和位置），阈值 1.0 将匹配任何内容。
    threshold: 0.4,
    // 匹配长度超过这个值的才会被认为是匹配的
    minMatchCharLength: 1,
    // 将被搜索的键列表。 这支持嵌套路径、加权搜索、在字符串和对象数组中搜索。
    // name：搜索的键
    // weight：对应的权重
    keys: [
      {
        name: 'title',
        weight: 0.7
      },
      {
        name: 'path',
        weight: 0.3
      }
    ]
  })
}
initFuse(searchPool.value)

/**
 * 关闭 search 的处理事件
 */
const onClose = () => {
  headerSearchSelectRef.value.blur()
  isShow.value = false
  searchOptions.value = []
}
/**
 * 监听 search 打开，处理 close 事件
 */
watch(isShow, val => {
  if (val) {
    document.body.addEventListener('click', onClose)
  } else {
    document.body.removeEventListener('click', onClose)
  }
})

// 处理国际化
watchSwitchLang(() => {
  searchPool = computed(() => {
    const filterRoutes = filterRouters(router.getRoutes())
    return generateRoutes(filterRoutes)
  })
  initFuse(searchPool.value)
})
</script>
```

这里用了`fuse.js`来做模糊匹配，

###### tagsview

`tgas` 就是位于 `appmain` 之上的标签，然后再加上动画和缓存，可以看下[官方文档](https://router.vuejs.org/zh/guide/advanced/transitions.html#%E5%9F%BA%E4%BA%8E%E8%B7%AF%E7%94%B1%E7%9A%84%E5%8A%A8%E6%80%81%E8%BF%87%E6%B8%A1)

```vue
<template>
  <div class="tags-view-container">
    <el-scrollbar class="tags-view-wrapper">
      <router-link
        class="tags-view-item"
        :class="isActive(tag) ? 'active' : ''"
        :style="{
          backgroundColor: isActive(tag) ? $store.getters.cssVar.menuBg : '',
          borderColor: isActive(tag) ? $store.getters.cssVar.menuBg : ''
        }"
        v-for="(tag, index) in $store.getters.tagsViewList"
        :key="tag.fullPath"
        :to="{ path: tag.fullPath }"
        @contextmenu.prevent="openMenu($event, index)"
      >
        {{ tag.title }}
        <i
          v-show="!isActive(tag)"
          class="el-icon-close"
          @click.prevent.stop="onCloseClick(index)"
        />
      </router-link>
    </el-scrollbar>
  </div>
</template>
```



##### 用户权限处理

 说道权限，得提一下`RBAC（Role-Based Access Control）` ，即基于角色的访问控制，是一种广泛应用于信息系统安全领域的访问控制机制。 

核心概念主要包括用户（User）、角色（Role）、权限（Permission）和对象（Object）。

1. **用户（User）**：系统中的实际操作者，可以是个人或组织。用户是权限的拥有者，通过被分配到特定的角色来获得相应的权限。
2. **角色（Role）**：代表一组权限集合，通常与组织中的职位或职能相对应。角色是RBAC中的关键概念，它简化了权限管理，因为权限是分配给角色的，而不是直接分配给用户。
3. **权限（Permission）**：允许执行特定操作的权利，如读取、写入、删除等。权限定义了用户对特定对象的操作能力。
4. **对象（Object）**：系统中的资源，如文件、数据库记录、API接口等。用户通过权限对对象进行操作。

在RBAC中，权限不再直接分配给用户，而是与角色相关联。用户通过成为适当角色的成员，从而获得该角色的权限。这种设计使得角色的创建、修改和删除变得相对简单，同时也便于用户的权限管理。 

在这个项目中，权限分为一级权限和二级权限，一级权限是指页面权限，二级权限指的是功能权限。实际上页面权限在前面已经处理了，在登录鉴权那里：

```js
if (!store.getters.hasUserInfo) {
    // 触发获取用户信息的 action，并获取用户当前权限
    const { permission } = await store.dispatch('user/getUserInfo')
    // 处理用户权限，筛选出需要添加的权限
    const filterRoutes = await store.dispatch(
    'permission/filterRoutes',
    permission.menus
    )
    // 利用 addRoute 循环添加
    filterRoutes.forEach(item => {
    router.addRoute(item)
    })
    // 添加完动态路由之后，需要在进行一次主动跳转
    return next(to.path)
}
```

这段代码是在全局路由守卫里，每次路由跳转都会调用一下，调用用户信息接口，拿到权限列表，根据这个权限列表去匹配路由，然后再动态添加到路由表中，这样只有相关权限的页面才能看的见，

对于功能权限，实际上就是按钮是否可见，这里采用了自定义指令来实现的。

```js
import store from '@/store'

function checkPermission(el, binding) {
  // 获取绑定的值，此处为权限
  const { value } = binding
  // 获取所有的功能指令
  const points = store.getters.userInfo.permission.points
  // 当传入的指令集为数组时
  if (value && value instanceof Array) {
    // 匹配对应的指令
    const hasPermission = points.some(point => {
      return value.includes(point)
    })
    // 如果无法匹配，则表示当前用户无该指令，那么删除对应的功能按钮
    if (!hasPermission) {
      el.parentNode && el.parentNode.removeChild(el)
    }
  } else {
    // eslint-disabled-next-line
    throw new Error('v-permission value is ["admin","editor"]')
  }
}

export default {
  // 在绑定元素的父组件被挂载后调用
  mounted(el, binding) {
    checkPermission(el, binding)
  },
  // 在包含组件的 VNode 及其子组件的 VNode 更新后调用
  update(el, binding) {
    checkPermission(el, binding)
  }
}

```

绑定下改指令

```js
import print from 'vue3-print-nb'
import permission from './permission'

export default app => {
  app.use(print)
  app.directive('permission', permission)
}
```

在`mian.js`中进行注册

```js
installDirective(app)
```

后续使用的话，直接这样就可以了

```vue
<el-button
    ...
    v-permission="['distributePermission']"
>
{{ $t('msg.role.assignPermissions') }}
</el-button>
```















