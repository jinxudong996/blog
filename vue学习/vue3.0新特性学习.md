##### vue3初探

首先使用vue-cli创建一个vue3项目，在APP.vue中写下如下代码：

```html
<template>
  <div id="#app">
    <img src="./assets/logo.png" alt="">
    <h1>{{count}}</h1>
    <button @click="increase">+1</button>
  </div>
</template>

<script lang="ts">
import {ref} from 'vue'

export default {
  name: 'App',
  setup() {
    const count = ref(0)
    const increase = () => {
      count.value++
    }
    return {
      count,
      increase
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

```

运行项目，即可以看到点击按钮，count会自动加1.

这里有两个vue3新加的函数，详细看vue[文档](https://v3.cn.vuejs.org/guide/composition-api-setup.html)

首先学习下组合式API，由于mixin存在属性冲突、无法传参等问题，vue3添加了组合式API这一概念，将页面中重复的部分连同其功能一起提取为可重用的代码段，来增加我们的应用的可维护性和灵活性。

- setup

  这个函数会在组件创建之前执行，接受两个参数props和content

  - props就是组件中的props，是一个响应式的对象，不能使用ES6的解构，会丢失它的响应式
  - content，一个普通的js对象，包含了attrs、slots、emit和expose函数。，

- ref，该函数可以申明一个响应式对象。

vue3将组件的计算属性、方法、生命周期钩子都放到了setup中。文档原文： 此外，我们将 `setup` 返回的所有内容都暴露给组件的其余部分 (计算属性、方法、生命周期钩子等等) 以及组件的模板。 

##### 模块加载实例

接下来写一个添加loader的模块：即在发接口前有一个状态判断，发送完成后又切成了另一个状态，看下代码：

```javascript
import { ref } from 'vue'
import axios from 'axios'

function useURLLoader<T>(url: string) {
  const result = ref<T | null>(null)
  const loading = ref(true)
  const loaded = ref(false)
  const error = ref(null)

  axios.get(url).then((rawData) => {
    loading.value = false
    loaded.value = true
    result.value = rawData.data
  }).catch(e => {
    error.value = e
    loading.value = false
  })
  return {
    result,
    loading,
    error,
    loaded
  }
}

export default useURLLoader
```

这里定义了四个变量：result作为请求的结果；loading作为加载前的标志，默认为true，加载到数据后设置为false；loaded和loading刚好相反，默认为false，加载成功后设置为true；error存储失败信息。

使用时：

```html
<template>
  <div id="#app">
    <img src="./assets/logo.png" alt="">
    <h1>{{count}}</h1>
    <button @click="increase">+1</button>
    <div>..............................................</div>
    <h1 v-if="loading">loading.....</h1>
    <img v-if="loaded" :src="result.message" alt="">
  </div>
</template>

<script lang="ts">
import {ref,watch} from 'vue'
import useURLLoader from './hooks/useURLLoader'

interface DogResult {
  message: string;
  status: string;
}

export default {
  name: 'App',
  setup() {
    const { result, loading, loaded } = useURLLoader<DogResult>('https://dog.ceo/api/breeds/image/random')
    watch(result, () => {
      if (result.value) {
        console.log('value', result.value.message)
      }
    })
    const count = ref(0)
    const increase = () => {
      count.value++
    }
    return {
      count,
      increase,
      result,
      loading,
      loaded
    }
  }
}
</script>
```

刷新页面即可看到loading结束后出来一张图片。

这里用到了ts的[泛型](https://juejin.cn/post/7067117967749677087#heading-42)。泛型就是为了考虑可重用性，组件不仅能够支持当前的数据类型，同时也能支持未来的数据类型。个人理解就是：目前我也不确定这个是啥类型，但我一旦指定了他是啥类型，就不能更改了，有着很大的灵活性。某种程度上来说，泛型就是充当占位符的作用。

##### teleport

接下来我么能实现一个简易的dialog组件。

```javascript
<template>
  <div id="center">
    <h2><slot>this is a modal</slot></h2>
  </div>
</template>
<script lang="ts">
export default {

}
</script>
<style>
  #center {
    width: 200px;
    height: 200px;
    border: 2px solid black;
    background: white;
    position: fixed;
    left: 50%;
    top: 50%;
    margin-left: -100px;
    margin-top: -100px;
  }
</style>

```

然后再APP.vue中注册以下，打开浏览器的Elements，就会发现我们的dialog在#app的下面，然而dialog被包裹在其他组件中，很容易受到干扰，而且样式也在其他组件中，很容易变得混乱。我们使用teleport来解决这个问题。

teleport是vue3新添加的一个默认组件，详细请看[文档](https://v3.cn.vuejs.org/guide/teleport.html#%E4%B8%8E-vue-components-%E4%B8%80%E8%B5%B7%E4%BD%BF%E7%94%A8)。 Vue 鼓励我们通过将 UI 和相关行为封装到组件中来构建 UI。我们可以将它们嵌套在另一个内部，以构建一个组成应用程序 UI 的树。他有一个to属性，表明挂载的dom节点。用teleport来更改下我们的代码：

在`public/index.html`中添加：

```
<div id="app"></div>
<div id="modal"></div>
```

这个`id=’model‘`的标签就是我们即将插入的dialog，在用teleport标签将代码包裹下：

```html
<template>
<teleport to="#dialog">
  <div id="center">
    <h2><slot>this is a modal</slot></h2>
  </div>
</teleport>
</template>
```

打开浏览器就可以看到我们的dialog已经和#app平级。

[代码地址](https://github.com/jinxudong996/blog/tree/main/ts%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/code/project/vue3-basic)



























