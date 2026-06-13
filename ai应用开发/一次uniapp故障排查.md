最近在开发uniapp，虽然第一次写，但是有vue开发经验，也没觉得有啥不一样的，上手还是比较简单的，但是明显我还是低估了uniapp的复杂度，这东西难点不在于业务开发，而是各个不同机型的适配，相比于传统的web开发，还是繁琐了很多。

业务开发中遇到了一个蛮有趣的问题，这里总结下。

##### 背景与环境

首先简单的描述下背景：就是在app登出的时候，发现了苹果6Plus在退出登录时表现不一样的地方，H5和安卓以及苹果16、ipad都表现正常，就是点击退出登录按钮，弹出一个弹窗，点击退出登录，跳转到到登录页，很常规的一个操作了，但是在苹果6Plus机型上，出现了异常，弹窗点击不动，页面出现了卡死，只能杀死应用重新进入。

这里贴下相关代码：

```js
message.comform({
    msg:"确定退出登录嘛",
    title:"退出登录"
}).then(res => {
    await userStore.logout()
    uni.redirectTo({
        url:'/pages/login/index'
    })
})
```

这里就是清除下`userStore`中的状态，然后就跳转路由到登录页。

> 这里总结下uniapp路由跳转的方式
>
> 1. uni.navigateTo  保留当掐你页面，跳转到某个应用内的页面
>
>    ```js
>    // 带参数跳转
>    uni.navigateTo({
>      url: '/pages/detail/detail?id=123&name=test'
>    })
>    
>    // 对象参数（需要编码）
>    uni.navigateTo({
>      url: '/pages/detail/detail?data=' + encodeURIComponent(JSON.stringify({
>        id: 123,
>        name: 'test'
>      }))
>    })
>    ```
>
> 2. uni.redirectTo 关闭当前页面 跳转到应用内的某个页面
>
>    ```js
>    uni.redirectTo({
>      url: '/pages/home/home'
>    })
>    ```
>
> 3. uni.reLaunch 关闭所有页面，打开到应用内的某个页面
>
>    ```js
>    uni.reLaunch({
>      url: '/pages/index/index'
>    })
>    ```
>
> 4. uni.switchTab 跳转到tabBar页面，并关闭其他所有非tabBar页面
>
>    ```js
>    uni.switchTab({
>      url: '/pages/home/home'
>    })
>    ```
>
> 5. uni.navigateBack  返回上一级或者多级页面
>
>    ```js
>    // 返回上一页
>    uni.navigateBack()
>    
>    // 返回多级页面
>    uni.navigateBack({
>      delta: 2  // 返回2级
>    })
>    ```

其中`logout`也是比较简单了，代码如下：

```js
const layout = async () => { 
    removeToken()
    resetState()
}
```

也就是登录前移除token和store中的一些状态，看代码没有任何问题，但是就是在苹果6Plus中出现卡顿，很费解，光看代码看不出任何问题，就带着问题问了下gpt，知道了`WKWebView 导航队列锁`这个东西。

##### WKWebView 导航队列锁

 `WKWebView` 导航队列锁定是 WebKit 内核中的一个**线程安全机制**，旨在防止在页面加载过程中的竞态条件。但在老版本中，这个机制实现得过于保守，导致并发导航操作容易被阻塞。 

主要有这么几个场景会触发

1. 快速连续导航调用

   ```js
   // 微观时序问题 - 导航竞争
   const startTime = performance.now();
   
   // 导航请求1 - 第0ms
   uni.navigateTo({ url: '/pageA' });
   
   // 在导航1还未完成状态转换时...
   setTimeout(() => {
       // 导航请求2 - 第5ms (此时导航1可能还在 WKNavigationStateScheduled)
       uni.navigateTo({ url: '/pageB' });
   }, 5);
   ```

   

2. 资源加载与导航竞争

   ```
   // WebKit 内部资源加载时序
   - (void)startNavigation:(WKNavigation *)navigation {
       [self acquireNavigationLock]; // 获取导航锁
       
       // 开始加载主文档
       [self loadMainDocument];
       
       // 此时如果主文档中有同步资源请求
       // <script src="sync-script.js"></script>
       // 资源加载会阻塞导航锁释放
       
       [self releaseNavigationLock]; // 延迟释放！
   }
   ```

   

3. js桥接与导航交互

   ```js
   // uni-app 框架层可能的问题
   // 1. 页面生命周期钩子与导航竞争
   export default {
       onLoad() {
           // 在 onLoad 中执行耗时操作
           this.loadHeavyData(); // 阻塞导航完成
       },
       
       onShow() {
           // 触发 UI 更新，需要渲染锁
           this.startAnimation(); 
       }
   }
   
   ```

   这个实例中，onLoad的触发时机是页面首次创建时 ， onShow触发是页面显示的时候会触发，当onLoad中执行loadHeavyData耗时操作时，等页面显示执行onShow中的startAnimation就会导致竞争资源，就会触发队列锁，导致页面卡死，比较好的方法就是让他们再一个方法中执行，然后将他们的步骤拆分下，比如这样：

   ```js
   onLoad() {
   	// 阶段1: 立即执行 (导航锁持有期间)
   	this.initUIState();
   
   	// 阶段2: 延迟执行 (导航锁释放后)
   	this.deferHeavyTask();
   
   	// 阶段3: 空闲时执行
   	this.idleNonCriticalTask();
   },
   ```

4. css、js动画与js冲突

   ```js
   function startAnimation() {
       const element = document.querySelector('.animated');
       element.style.transform = 'translateX(0)';
       
       // 触发 CSS 动画
       requestAnimationFrame(() => {
           element.style.transform = 'translateX(100px)';
           
           // 在同一帧内触发导航
           uni.navigateTo({ url: '/next' }); // 危险！
       });
   }
   ```

然后回到项目相关代码，似乎也没有很大的计算量导致资源竞争，触发队列锁，看下gpt5优化后的代码：

```js
const clicking = ref(false)
const handleLogout = async () => {
	if(clicking.value) return
	click.value = false
	await message.confirm({msg:'确定退出登录？',title:'退出登录'})
	useStore.logOut()
	setTimeout(() => clicking.value=false,300)
}
```

```js
const delay = ms => new Promise(r => setTimeout(r,ms))
const loggingOut = ref(false)
const LogOut = async () => {
    if(loggingOut.value) return
    loggingOut.value = true
    removeToken()
    resetState()
    uni.$emit?.('router:unlock')
    uni.$emit?.('ui:closs-popups')
    
    await delay(220)
    
    try {uni.reLaunch({url:'/pages/login/index'}) } catch {}
    setTimeout(() => try{uni.relaunch({url:'/pages/login/index'}) catch {}, 700)
    
    loggingOut.value = false
}
```

看了下代码，似乎也没有啥变更，只是都加了个开关，然后加了个延时操作，但是问题确实解决了。确实非常奇怪的问题。













































##### 