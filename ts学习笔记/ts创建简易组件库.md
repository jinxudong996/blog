vue3+TS搭建一个自己的组件库。

#### 前置

首先下载vue-cli，搭建我们的环境，`vue-create-luckyUi`，选择vue3和TypeScript 。在src目录下创建`package`作为组件目录。再安装`bootstrap`，用bootstrap里面的样式来完成我们的组件。

#### 组件编写

##### dropdown

首先查看boorstrap[文档](https://v4.bootcss.com/docs/components/dropdowns/)，是这样用的

```javascript
<div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-expanded="false">
    Dropdown button
  </button>
  <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
    <a class="dropdown-item" href="#">Action</a>
    <a class="dropdown-item" href="#">Another action</a>
    <a class="dropdown-item" href="#">Something else here</a>
  </div>
</div>
```

首先那个button按钮就是我们dropdown按钮的内容，将这部分作为属性传入，而dropdown-menu的内容是作为dropdown-item的，明显这里不能固定写三个，这里就用插槽占位，再封装一个dropdown-item组件。

首先dropdown组件内容如下：

```javascript
<template>
  <div class="dropdown" ref="dropdownRef">
    <a
      href="#"
      class="btn btn-outline-light my-2 dropdown-toggle"
      @click.prevent="toggleOpen"
    >
      {{ title }}
    </a>
    <ul class="dropdown-menu" :style="{ display: 'block' }" v-if="isOpen">
      <slot></slot>
    </ul>
  </div>
</template>
```

dropdown-item的内容就是：

```javascript
<template>
  <li
    class="dropdown-option"
    :class="{'is-disabled': disabled}"
  >
    <slot></slot>
  </li>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: "DropdownItem",
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  }
})
</script>

<style>
.dropdown-option.is-disabled * {
  color: #6c757d;
  pointer-events: none;
  background-color: transparent;
}
</style>

```

还要实现一个点击dropdown，dropdown-item会随之收起来的功能，这个比较简单，在dropdown上绑定一个点击事件来控制变量isOpen为true或者false，在加上v-if即可实现功能。接下来还要实现一个点击页面的其他地方也能实现dropdown-item收缩，这里有两个思路：

- 首先在document上添加一个click事件，一旦触发就设置isOpen为false，给dropdown也添加一个点击事件，加上一个事件修饰符`stop`来阻止事件冒泡，这样除了点击dropdown意外的任何地方，document都会触发点击事件。
- 第二个思路就是让事件冒泡到document，通过判断事件对象包不包括我们的目标对象，如果不包括说明点击的是页面的其他地方，就设置isOpen为false。这里用了到了组合式api，新建文件`package/hooks/useClickOutside.ts`，

```javascript
import { ref, onMounted, onUnmounted, Ref } from 'vue'

const useClickOutside = (elementRef: Ref<null | HTMLElement>) => {
  const isClickOutside = ref(false)
  const handler = (e: MouseEvent) => {
    if (elementRef.value) {
      if (elementRef.value.contains(e.target as HTMLElement)) {
        isClickOutside.value = false
      } else {
        isClickOutside.value = true
      }
    }
  }
  onMounted(() => {
    document.addEventListener('click', handler)
  })
  onUnmounted(() => {
    document.removeEventListener('click', handler)
  })
  return isClickOutside
}

export default useClickOutside

```

然后直接导入即可使用定义的useClickOutside函数。这里监听isClickOutside的状态来更改isOpen的状态。

```javascript
import useClickOutside from "../hooks/useClickOutside";
...
const isClickOutside = useClickOutside(dropdownRef);

watch(isClickOutside, () => {
  if (isOpen.value && isClickOutside.value) {
    isOpen.value = false;
  }
});
```

##### form

首先看下[文档](https://v4.bootcss.com/docs/components/forms/)用法

```html
<form>
  <div class="form-group">
    <label for="exampleInputEmail1">Email address</label>
    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
    <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
  </div>
  <div class="form-group">
    <label for="exampleInputPassword1">Password</label>
    <input type="password" class="form-control" id="exampleInputPassword1">
  </div>
  <div class="form-group form-check">
    <input type="checkbox" class="form-check-input" id="exampleCheck1">
    <label class="form-check-label" for="exampleCheck1">Check me out</label>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

首先编写ValidateForm组件：

```html
<template>
  <form class="validate-form-container">
    <slot name="default"></slot>
    <div class="submit-area" @click.prevent="submitForm">
      <slot name="submit">
        <button type="submit" class="btn btn-primary">提交</button>
      </slot>
    </div>
  </form>
</template>

<script lang="ts">
import { defineComponent, onUnmounted } from 'vue'
import mitt from 'mitt'
type ValidateFunc = () => boolean
export const emitter = mitt()
export default defineComponent({
  emits: ['form-submit'],
  setup(props, context) {
    let funcArr: ValidateFunc[] = []
    const submitForm = () => {
      const result = funcArr.map(func => func()).every(result => result)
      context.emit('form-submit', result)
    }
    const callback = (func?: ValidateFunc) => {
      if (func) {
        funcArr.push(func)
      }
    }
    emitter.on('form-item-created', callback)
    onUnmounted(() => {
      emitter.off('form-item-created', callback)
      funcArr = []
    })
    return {
      submitForm
    }
  }
})
</script>

```

接着编写ValidateInput.vue组件：

```javascript
<template>
  <div class="validate-input-container pb-3">
    <input
      class="form-control"
      :class="{'is-invalid': inputRef.error}"
      @blur="validateInput"
      v-model="inputRef.val"
      v-bind="$attrs"
    >
    <span v-if="inputRef.error" class="invalid-feedback">{{inputRef.message}}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, PropType, onMounted, computed } from 'vue'
import { emitter } from './ValidateForm.vue'
const emailReg = /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
interface RuleProp {
  type: 'required' | 'email' | 'custom';
  message: string;
  validator?: () => boolean;
}
export type RulesProp = RuleProp[]
export type TagType = 'input'
export default defineComponent({
  props: {
    rules: Array as PropType<RulesProp>,
    modelValue: String,
    tag: {
      type: String as PropType<TagType>,
      default: 'input'
    }
  },
  inheritAttrs: false,
  setup(props, context) {
    const inputRef = reactive({
      val: computed({
        get: () => props.modelValue || '',
        set: val => {
          context.emit('update:modelValue', val)
        }
      }),
      error: false,
      message: ''
    })
    const validateInput = () => {
      if (props.rules) {
        const allPassed = props.rules.every(rule => {
          let passed = true
          inputRef.message = rule.message
          switch (rule.type) {
            case 'required':
              passed = (inputRef.val.trim() !== '')
              break
            case 'email':
              passed = emailReg.test(inputRef.val)
              break
            case 'custom':
              passed = rule.validator ? rule.validator() : true
              break
            default:
              break
          }
          return passed
        })
        inputRef.error = !allPassed
        return allPassed
      }
      return true
    }
    onMounted(() => {
      emitter.emit('form-item-created', validateInput)
    })
    return {
      inputRef,
      validateInput
    }
  }
})
</script>

```

这里核心的地方有两点：

- 自定义组件实现v-model，vue2中自定义组件实现v-mdel必须要绑定一个`value`属性和`input事件`，在input事件中将输入的值传递给`value`。在vue3中就需要绑定一个`modelValue`和`update:modelValue事件`
- 还有就是父子组件之间的传值问题，因为有插槽，没办法使用常规的属性传值，这里使用的事件传值采用了一个第三方库[mitt](https://github.com/developit/mitt)。在父组件中通过`emitter.on('form-item-created', callback)`来注册事件，在子组件中通过`emitter.emit('form-item-created', validateInput)`触发事件。

#### 验证

新建文件`package/index.ts`

```javascript
import 'bootstrap/dist/css/bootstrap.min.css'

//导入组件
import Dropdown from "./Dropdown/Dropdown.vue";
import DropdownItem from "./Dropdown/DropdownItem.vue";

const components = [
  Dropdown,
  DropdownItem
]

const install = (Vue: any) => {
  components.forEach((_: any) => {
    Vue.component(_.name, _);
  });
};

export default {
  install
};
```

将写的组件依次导入，然后定义一个install函数，该函数有一个Vue实例的参数，在函数中依次遍历我们的导入组件数组，然后将组件挂载到vue实例上，导出install函数。

在根目录下的main.ts上使用我们的新组件：

```javascript
import { createApp } from 'vue'
import App from './App.vue'

import luckyUi from './package/index';

const app = createApp(App)

app.use(luckyUi);

app.mount('#app')
```

在app.vue中进行测试：

```html
<template>
  <div>
    <div class="dropdown">
      <!-- 测试dropdown -->
      <dropdown :title="`你好啊`">
        <dropdown-item><a href="#">王大</a> </dropdown-item>
        <dropdown-item>
          <a href="#">王二</a>
        </dropdown-item>
        <dropdown-item disabled
          ><a href="#" class="dropdown-item">王三</a></dropdown-item
        >
        <dropdown-item
          ><a href="#" class="dropdown-item">王四</a></dropdown-item
        >
      </dropdown>
    </div>
  </div>
</template>
```

最后使用vue自带的脚手架进行打包，详细可看[文档](https://cli.vuejs.org/zh/guide/cli-service.html#vue-cli-service-build)。

在package中配置打包命令：

```
"lib": "vue-cli-service build --target lib --name lucky-ui ./src/package/index.ts"
```

运行`npm run lib`即可在dist目录下查看。