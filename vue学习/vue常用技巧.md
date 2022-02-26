##### extend使用技巧

这是一个全局API，详细可查看[文档](https://cn.vuejs.org/v2/api/#Vue-extend)。

>  使用基础 Vue 构造器，创建一个“子类”。参数是一个包含组件选项的对象。 

经常使用Vue.extend来创建一个组件，

```javascript
var Profile = Vue.extend({
  template: '<p>{{firstName}} {{lastName}} aka {{alias}}</p>',
  data: function () {
    return {
      firstName: 'Walter',
      lastName: 'White',
      alias: 'Heisenberg'
    }
  }
})
```

接下来封装一个简易的dialog，将其挂载到body下面。

```html
//简易的dialog  alert.vue
<template>
  <div class="grid">
    <h1 class="head">这里是标题</h1>
    <div @click="close">{{ cancelText }}</div>
    <div @click="onSureClick">{{ sureText }}</div>
  </div>
</template>
<script>
export default {
  name:'alert',
  props: {
    close: {
      type: Function,
      default: () => {},
    },
    cancelText: {
      type: String,
      default: "取消",
    },
    sureText: {
      type: String,
      default: "确定",
    },
  },
  methods: {
    onSureClick() {
      // 其他逻辑
      console.log('onSureClick')
    },
  },
};
</script>
```

封装一个函数，用于挂载组件到目标标签上，说是挂载，实际上就是替换：

```javascript
export default function extendComponents(component,callback,Vue){
  const Action = Vue.extend(component)
  const div = document.createElement('div')
  document.body.appendChild(div)
  const ele = new Action({
    propsData:{
      cancelText:'cancel1',
      sureText:'sure2',
      close:()=>{
        ele.$el.remove()
        callback&&callback()
      }
    }
  }).$mount(div)
}

```

来验证一下：

```javascript
import extendComponents from './hooks/extendComponents.js'
import alert from './components/alert.vue'

extendComponents(alert,() => {
  console.log('入口挂载')
},Vue)
```

打开浏览器的element，即可以看到我们的组件被挂载到了body下面。

##### 几个有用的自定义指令

在需要对dom元素进行更底层的操作时，就需要用到自定义指令，详细柯可看[文档](https://cn.vuejs.org/v2/guide/custom-directive.html)。

有两种注册自定义指令的方式，全局注册和局部注册。

- 全局注册

  ```javascript
  // 注册一个全局自定义指令 `v-focus`
  Vue.directive('focus', {
    // 当被绑定的元素插入到 DOM 中时……
    inserted: function (el) {
      // 聚焦元素
      el.focus()
    }
  })
  ```

  

- 局部注册

  ```javascript
  //在组件中定义
  directives: {
    focus: {
      // 指令的定义
      inserted: function (el) {
        el.focus()
      }
    }
  }
  ```

一个指定对象可以接受五个钩子函数

- bind，只调用一次，指令第一次绑定到元素时调用
- inserted，被绑定元素插入父节点时调用
- update，所在组件的vnode更新时调用
- componentUpdated，指令所在组件的vnode及其子vnode全部更新时调用
- unbind，指令与元素解绑时调用

钩子函数会被传入以下参数

- el，指令当前所绑定的对象
- binding，一个对象，包含name，value等属性
- vnode，vue编译生成的虚拟dom
- oldVnode，上一个虚拟节点，只在update和componentUpdate中调用

接下里做几个有意思的自定义指令。

- 点击复制

  这里主要通过bind钩子函数第二个参数的value属性拿的目标上的内容，然后通过动态创建一个textarea标签，将拿到的值赋值给textarea，调用`textarea.select()`选中内容，通过`document.execCommand("Copy")`进行复制。

  代码如下

  ```html
  <template>
    <button v-copy="copyText">复制</button>
  </template>
  
  <script>
  export default {
    directives:{
      copy:{
        bind(el, { value }) {
        el.$value = value;
        el.handler = () => {
          if (!el.$value) {
            // 值为空的时候，给出提示。可根据项目UI仔细设计
            console.log("无复制内容");
            return;
          }
          // 动态创建 textarea 标签
          const textarea = document.createElement("textarea");
          // 将该 textarea 设为 readonly 防止 iOS 下自动唤起键盘，同时将 textarea 移出可视区域
          textarea.readOnly = "readonly";
          textarea.style.position = "absolute";
          textarea.style.left = "-9999px";
          // 将要 copy 的值赋给 textarea 标签的 value 属性
          textarea.value = el.$value;
          // 将 textarea 插入到 body 中
          document.body.appendChild(textarea);
          // 选中值并复制
          textarea.select();
          const result = document.execCommand("Copy");
          if (result) {
            console.log("复制成功",value);
          }
          document.body.removeChild(textarea);
        };
        // 绑定点击事件，就是所谓的一键 copy 啦
        el.addEventListener("click", el.handler);
      },
      // 当传进来的值更新的时候触发
      componentUpdated(el, { value }) {
        el.$value = value;
      },
      // 指令与元素解绑的时候，移除事件绑定
      unbind(el) {
        el.removeEventListener("click", el.handler);
      },
      }
    },
    data() {
      return {
        copyText: "a copy directives",
      };
    },
  };
  </script>
  ```

  

- 表单校验

  在使用到表单组件时，经常会对表单的输入内容进行校验，一般做法时在@change函数上添加判断：

  ```html
  <template>
    <input type="text" v-model="note" @change="vaidateEmoji" />
  </template>
  
  <script>
    export default {
      methods: {
        vaidateEmoji() {
          var reg = /[^\u4E00-\u9FA5|\d|\a-zA-Z|\r\n\s,.?!，。？！…—&$=()-+/*{}[\]]|\s/g
          this.note = this.note.replace(reg, '')
        },
      },
    }
  </script>
  ```

  如果表单过多，得一个个添加，可以使用自定义组件来解决这个问题。

  ```html
  <template>
    <input type="text" v-model="note" v-validate />
  </template>
  
  <script>
  
  let findEle = (parent, type) => {
    return parent.tagName.toLowerCase() === type ? parent : parent.querySelector(type)
  }
  
  const trigger = (el, type) => {
    const e = document.createEvent('HTMLEvents')
    e.initEvent(type, true, true)
    el.dispatchEvent(e)
  }
  
  export default {
    data(){
      return{
        note:''
      }
    },
    directives: {
      validate: {
        bind: function (el, binding, vnode) {
          // 正则规则可根据需求自定义
          var regRule =
            /[^\u4E00-\u9FA5|\d|\a-zA-Z|\r\n\s,.?!，。？！…—&$=()-+/*{}[\]]|\s/g;
          let $inp = findEle(el, "input");
          el.$inp = $inp;
          $inp.handle = function () {
            let val = $inp.value;
            $inp.value = val.replace(regRule, "");
  
            trigger($inp, "input");
          };
          $inp.addEventListener("keyup", $inp.handle);
        },
        unbind: function (el) {
          el.$inp.removeEventListener("keyup", el.$inp.handle);
        },
      },
    },
    methods: {
      vaidateEmoji() {
        var reg =
          /[^\u4E00-\u9FA5|\d|\a-zA-Z|\r\n\s,.?!，。？！…—&$=()-+/*{}[\]]|\s/g;
        this.note = this.note.replace(reg, "");
      },
    },
  };
  </script>
  ```



##### @hooks

父组件监听子组件的生命周期，常用的方法可以在子组件的生命周期里用$emit向父组件抛出一个事件来监听，代码如下：

```javascript
// Parent.vue
<Child @mounted="doSomething"/>
    
// Child.vue
mounted() {
  this.$emit("mounted");
}
```

如果子组件特别复杂，也可以通过hooks监听子组件事件

```javascript
//  Parent.vue
<Child @hook:mounted="doSomething" ></Child>

doSomething() {
   console.log('父组件监听到 mounted 钩子函数 ...');
},
    
//  Child.vue
mounted(){
   console.log('子组件触发 mounted 钩子函数 ...');
},   

```

#####  observable 创建跨组件状态存储器 

使用vuex还是比较繁琐的，如果想简单点，可以使用observable来创建一个小型的vuex。

```javascript
import Vue from 'vue'

// 通过Vue.observable创建一个可响应的对象
export const store = Vue.observable({
  userInfo: {},
  roleIds: []
})

// 定义 mutations, 修改属性
export const mutations = {
  setUserInfo(userInfo) {
    store.userInfo = userInfo
  },
  setRoleIds(roleIds) {
    store.roleIds = roleIds
  }
}
```

```html
<template>
  <div>
    {{ userInfo.name }}
  </div>
</template>
<script>
import { store, mutations } from '../store'
export default {
  computed: {
    userInfo() {
      return store.userInfo
    }
  },
  created() {
    mutations.setUserInfo({
      name: 'nick'
    })
  }
}
</script>

```

