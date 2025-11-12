## 一、前言：为什么选择 uni-app？

在如今的前端生态中，跨端开发已经成为趋势。无论是 H5、小程序，还是原生 App，企业都希望**“一套代码，多端运行”**。

在众多跨端框架中，**uni-app** 是国产方案的佼佼者。它基于 Vue 语法，支持编译到 **微信 / 支付宝 / 抖音小程序、H5、App（iOS/Android）** 等多个平台。对于前端开发者来说，几乎可以“零门槛”上手。

**为什么选择 uni-app：**

- ✅ 学习成本低（Vue 语法）
- ✅ 支持多端（H5 + 小程序 + App）
- ✅ 官方维护稳定，生态丰富
- ✅ 支持 Vue3 + Vite

> 本文将从基础语法讲起，再深入运行机制、性能优化和原生扩展。
>  帮你从“能跑通项目”到“真正理解底层原理”。



## 二、快速上手：10 分钟跑通第一个项目

### 1️⃣ 环境准备

推荐使用官方 IDE **HBuilderX**，也可以用 VSCode + CLI。

`HBuilderX`是官方推荐的IDE，开箱即用，内置很好功能：

1. uni-app 项目模板；

2. 真机调试 / 预览 / 打包；

3. 语法高亮、API 提示；

4. 小程序、H5、App 的一键运行。

但是我在查看项目时发现这玩意老卡顿，根本没有VSCode好使。

所以使用vscode开发，再使用`HBuilderX`调试打包倒是个不错的选择。

直接使用官网提供的模板来创建项目

```
npx degit dcloudio/uni-preset-vue#vite my-vue3-project
```

然后下载依赖

```
pnpm install
```

运行项目，就可以查看h5版的

```
npm run dev:h5
```

### 2️⃣ 目录结构讲解

这里的目录和常规的vue项目都大差不差，但是也糅合了小程序的分割，比如在`pages.json`中定义路由

| 目录                | 说明                         |
| ------------------- | ---------------------------- |
| `src/pages/`        | 页面文件夹                   |
| `src/static/`       | 静态资源                     |
| `src/manifest.json` | 应用配置（如 App 包名）      |
| `src/pages.json`    | 路由与导航配置，和小程序一样 |
| `src/uni.scss`      | 全局样式变量                 |

------

### 3️⃣ 编写第一个页面

首先更改路由文件夹：

```json
{
	"pages": [ 
		{
			"path": "pages/index/index",
			"style": {
				"navigationBarTitleText": "uni-app"
			}
		},
		{
			"path": "pages/mine/index",
			"style": {
				"navigationBarTitleText": "uni-app"
			}
		}
	],
	"tabBar":{
		"list": [
			{
				"pagePath": "pages/index/index",
				"text": "首页"
			},
			{
				"pagePath": "pages/mine/index",
				"text": "我的"
			}
		],
		"selectedColor": "#FF0000",
		"color": "#000000",
		"backgroundColor": "#FFFFFF"
	},
	"globalStyle": {
		"navigationBarTextStyle": "black",
		"navigationBarTitleText": "uni-app",
		"navigationBarBackgroundColor": "#F8F8F8",
		"backgroundColor": "#F8F8F8"
	}
}
```

再默认的首页基础上添加了`pages/mine/index`文件，而且添加了`tabBar`，就是页面底部的按钮，和小程序原生写法一模一样。

`pages/mine/index`也是很简单的：

```vue
<template>
  <view class="container">
    <text>{{ msg }}</text>
  </view>
</template>

<script>
export default {
  data() {
    return { msg: "你好，uni-app,这里是我的模块" };
  },
};
</script>

<style scoped>
.container {
  text-align: center;
  margin-top: 50rpx;
  font-size: 32rpx;
}
</style>
```

运行`npm run dev:h5`就可以看到`h5`版本的页面了。





## 三、核心语法与开发规范

### 1️⃣ 基于 Vue 的开发体验

uni-app 完全兼容 Vue2/Vue3 语法：

```
<view v-if="isShow">{{ count }}</view>
<button @click="count++">增加</button>
```

常见生命周期：

| 生命周期 | 触发时机         |
| -------- | ---------------- |
| onLoad   | 页面加载时       |
| onReady  | 页面初次渲染完成 |
| onShow   | 页面显示时       |
| onHide   | 页面隐藏时       |

------

### 2️⃣ 页面与路由配置

在 `pages.json` 中注册页面：

```
{
  "pages": [
    { "path": "pages/index/index", "style": { "navigationBarTitleText": "首页" } }
  ]
}
```

跳转方式：

```
uni.navigateTo({ url: '/pages/detail/detail?id=1' })
```

------

### 3️⃣ 网络请求与封装

uni-app 内置 `uni.request`：

```
uni.request({
  url: 'https://api.example.com/data',
  success: res => { console.log(res.data) }
})
```

推荐封装统一接口：

```
export function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      ...options,
      success: res => resolve(res.data),
      fail: err => reject(err)
    })
  })
}
```

------

### 4️⃣ 样式与组件

- 使用 `rpx` 实现自适应布局（小程序标准单位）
- 支持全局样式和 CSS 变量
- 推荐使用官方组件库 uni-ui

------

## 四、跨端兼容性详解

跨端是 uni-app 的最大优势，也是最容易出坑的部分。

### 1️⃣ 平台差异

- **H5 端**：运行在浏览器中；
- **小程序端**：运行在微信等容器中；
- **App 端**：运行在 WebView 中。

### 2️⃣ 条件编译

uni-app 提供编译指令：

```
#ifdef MP-WEIXIN
wx.showToast({ title: '微信端' })
#endif

#ifdef H5
alert('H5端')
#endif
```

### 3️⃣ 常见兼容问题

- Web 特性（如 `window`、`document`）小程序端不可用；
- 第三方 npm 包中可能有平台限制；
- CSS 部分属性在 App 端表现不同。

> 🔧 建议在开发时保持“最小公约数”思维，尽量写跨端通用代码。



## 五、运行机制与编译原理（重点）

### 1️⃣ 编译原理概览

uni-app 会将 Vue 文件编译为对应平台的语言：

| 目标平台 | 编译产物         | 运行容器              |
| -------- | ---------------- | --------------------- |
| H5       | HTML + JS        | 浏览器                |
| 小程序   | WXML + WXSS + JS | 小程序引擎            |
| App      | HTML + JS        | WebView（内嵌浏览器） |

### 2️⃣ 运行机制图

```
你写的 Vue 源码
    ↓
uni-app 编译器
    ↓
生成不同平台代码（wxml/html/nvue）
    ↓
运行在各自引擎上（小程序引擎 / WebView）
```

### 3️⃣ JSBridge 通信机制

App 端无法直接访问系统 API（摄像头、蓝牙等），
 通过 **JSBridge** 让 JS 与原生交互。

```
JS 调用 uni.getLocation()
   ↓
JSBridge.send('getLocation')
   ↓
Native 调用系统 API
   ↓
结果通过 Bridge 回传给 JS
```

------

## 六、性能优化与包体积控制

### 1️⃣ 常见性能问题

- 页面切换卡顿；
- 图片加载慢；
- 频繁的 setData；
- H5 端包体积大。

### 2️⃣ 优化建议

- ✅ 使用虚拟滚动（`recycle-list`）；
- ✅ 图片懒加载；
- ✅ 按需分包；
- ✅ 复用组件，减少渲染层通信；
- ✅ 使用 `nvue` 页面提高性能。

### 3️⃣ 分包加载示例

```
{
  "subPackages": [
    {
      "root": "pages/user",
      "pages": ["profile", "setting"]
    }
  ]
}
```

------

## 七、原生能力衔接与插件开发

### 1️⃣ 官方原生 API 示例

```
uni.getSystemInfo({
  success: info => console.log(info.model)
})
```

### 2️⃣ 当官方 API 不够时：自定义原生插件

- 插件市场：https://ext.dcloud.net.cn/
- 也可以自己写：

#### Android 示例

```
@UniJSMethod(uiThread = true)
public void getBattery(CallbackContext callback) {
    BatteryManager bm = (BatteryManager) mUniSDKInstance.getContext().getSystemService(Context.BATTERY_SERVICE);
    int level = bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY);
    JSONObject data = new JSONObject();
    data.put("battery", level);
    callback.success(data);
}
```

JS 调用：

```
uni.requireNativePlugin('MyBattery').getBattery(res => {
  console.log('电量：', res.battery)
})
```

------

## 八、工程化与协作

- 使用 VSCode + CLI 开发（支持 Git）
- 配置多环境变量 `.env.dev / .env.prod`
- CI/CD 自动构建（Jenkins / GitHub Actions）

------

## 九、实战案例：跨端商城项目

- 首页：商品列表 + 搜索；
- 详情页：跨端跳转；
- 登录模块：App、小程序共用逻辑；
- 接口封装 + 数据缓存；
- 性能优化：虚拟列表 + 懒加载。

------

## 十、总结与展望

**uni-app 的优点：**

- Vue 语法友好；
- 生态成熟；
- 一套代码覆盖主流端。

**缺点：**

- 多端差异仍然存在；
- WebView 性能有限；
- 原生扩展有一定门槛。

> 🔮 未来趋势：
>  Vue3 + Vite 编译速度更快；
>  nvue 原生渲染性能提升显著。