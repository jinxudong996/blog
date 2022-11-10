##### 搭建项目

可以通过`npm create vite`来开始项目初始化，npm会自动下载`create-vite`这个包，随后就开始项目初始化的逻辑了，比如设置项目名称、项目的语言以及是否使用ts。这里就先用react+ts学习下vite。

搭建完项目后，可以看到项目的目录结构：

```javascript
├── index.html
├── package.json
├── pnpm-lock.yaml
├── src
│   ├── App.css
│   ├── App.tsx
│   ├── favicon.svg
│   ├── index.css
│   ├── logo.svg
│   ├── main.tsx
│   └── vite-env.d.ts
├── tsconfig.json
└── vite.config.ts
```

其中根目录线下的`index.html`就是我们的入口文件，在入口文件中引入了一个`main.tsx`文件，这就是我们的react入口文件，`Vite Dev Server`将浏览器不能识别的`import`语句编译成一个http请求， `Vite Dev Server` 会读取本地文件，返回浏览器可以解析的代码。当浏览器解析到新的 import 语句，又会发出新的请求，以此类推，直到所有的资源都加载完成。 

 Vite 所倡导的`no-bundle`理念的真正含义: 利用浏览器原生 ES 模块的支持，实现开发阶段的 Dev Server，进行模块的按需加载，而不是先整体打包再进行加载。 

##### 配置

vite配置可以通过命令行参数，比如`vite --prot=8888`，同样也可以配置文件，一般都放置在`vite.config.ts`作为配置文件。

目前我们这个项目的配置文件长这个样子：

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()]
})
```

在plugins中配置了官方的react插件，来提供react项目编译和热更新。

###### 入口配置

现在我们的入口文件是根目录下的`index.html`，如果想更改入口文件，可以指定root选项：

```javascript
import { defineConfig } from 'vite'
// 引入 path 包注意两点:
// 1. 为避免类型报错，你需要通过 `pnpm i @types/node -D` 安装类型
// 2. tsconfig.node.json 中设置 `allowSyntheticDefaultImports: true`，以允许下面的 default 导入方式
import path from 'path'
import react from '@vitejs/plugin-react'

export default defineConfig({
  // 手动指定项目根目录位置
  root: path.join(__dirname, 'src')
  plugins: [react()]
})
```

###### css配置

在项目中使用sass可以使用他的嵌套语法，定义变量，大大增强了样式语言的灵活性。我们可以再一个文件中定义一些全局变量： $theme-color: red，然后通过import语法导入：

```javascript
@import "../../variable";

.header {
  color: $theme-color;
}
```

每次使用都需要重新导入，可以在vite中做一个配置，让其变成全局变量：

```js
import { normalizePath } from 'vite';
// 如果类型报错，需要安装 @types/node: pnpm i @types/node -D
import path from 'path';

// 全局 scss 文件的路径
// 用 normalizePath 解决 window 下的路径问题
const variablePath = normalizePath(path.resolve('./src/variable.scss'));


export default defineConfig({
  // css 相关的配置
  css: {
    preprocessorOptions: {
      scss: {
        // additionalData 的内容会在每个 scss 文件的开头自动注入
        additionalData: `@import "${variablePath}";`
      }
    }
  }
})
```

同样也可以配置我们的css modules：

```javascript
export default {
  css: {
    modules: {
      // 一般我们可以通过 generateScopedName 属性来对生成的类名进行自定义
      // 其中，name 表示当前文件名，local 表示类名
      generateScopedName: "[name]__[local]___[hash:base64:5]"
    },
    preprocessorOptions: {
      // 省略预处理器配置
    }

  }
}
```

经常配置PostCSS来补充css前缀

```js
export default {
  css: {
    // 进行 PostCSS 配置
    postcss: {
      plugins: [
        autoprefixer({
          // 指定目标浏览器
          overrideBrowserslist: ['Chrome > 40', 'ff > 31', 'ie 11']
        })
      ]
    }
  }
}
```

































































