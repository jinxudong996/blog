

##### jsx语法

使用 React 就一定会写 JSX，它是一种 JavaScript 语法的扩展，React 使用它来描述用户界面长成什么样子。虽然它看起来非常像 HTML，但它确实是 JavaScript 。在 React 代码执行之前，Babel 会对将 JSX 编译为 React API.

```react
<div className="container">
  <h3>Hello React</h3>
  <p>React is great </p>
</div>
```

```react
React.createElement(
  "div",
  {
    className: "container"
  },
  React.createElement("h3", null, "Hello React"),
  React.createElement("p", null, "React is great")
);
```

JSX 被 Babel 编译为 React.createElement 方法的调用，被createElement()方法调用之后，返回的就是VirtualDOM。至于babel是如何编译jsx语法的，主要通过两个babel插件：

- @babel/plugin-syntax-jsx ： 使用这个插件，能够让 Babel 有效的解析 JSX 语法。
- @babel/plugin-transform-react-jsx ：这个插件内部调用了 @babel/plugin-syntax-jsx，可以把 React JSX 转化成 JS 能够识别的 createElement 格式。

 这里通过 api 的方式来模拟一下 Babel 处理 JSX 的流程

 第一步：创建 element.js，写下将测试的 JSX 代码，

```javascript
import React from 'react'

function TestComponent(){
    return <p> hello,React </p>
}
function Index(){
    return <div>
        <span>模拟 babel 处理 jsx 流程。</span>
        <TestComponent />
    </div>
}
export default Index
```

第二步： 新建文件 jsx.js 

```javascript
const fs = require('fs')
const babel = require("@babel/core")

/* 第一步：模拟读取文件内容。 */
fs.readFile('./element.js',(e,data)=>{ 
    const code = data.toString('utf-8')
    /* 第二步：转换 jsx 文件 */
    const result = babel.transformSync(code, {
        plugins: ["@babel/plugin-transform-react-jsx"],
    });
    /* 第三步：模拟重新写入内容。 */
    fs.writeFile('./element.js',result.code,function(){})
})
```

第三步：命令行运行jsx.js，看一下element.js内容

```javascript
import React from 'react';

function TestComponent() {
  return /*#__PURE__*/React.createElement("p", null, " hello,React ");
}

function Index() {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("span", null, "\u6A21\u62DF babel \u5904\u7406 jsx \u6D41\u7A0B\u3002"), /*#__PURE__*/React.createElement(TestComponent, null));
}
export default Index;
```

##### Virtual DOM 

DOM 提供了一组 JavaScript 接口用来遍历或者修改节点，这套接口包含了 getElementById、removeChild、appendChild 等方法。 举个例子：比如，我们可以调用document.body.appendChild(node)往 body 节点上添加一个元素，调用该 API 之后会引发一系列的连锁反应。首先渲染引擎会将 node 节点添加到 body 节点之上，然后触发样式计算、布局、绘制、栅格化、合成等任务，我们把这一过程称为重排。除了重排之外，还有可能引起重绘或者合成操作，形象地理解就是牵一发而动全身。另外，对于 DOM 的不当操作还有可能引发强制同步布局和布局抖动的问题，这些操作都会大大降低渲染效率。因此，对于 DOM 的操作我们时刻都需要非常小心谨慎。 

而虚拟DOM就是用JavaScript对象描述DOM对象，操作js对象消耗要比操作DOM对象小得多，需要更新视图时先用diff算法对比DOM对象，对比出变化后再更新当前的虚拟DOM，然后在去操作真实的DOM。

这里存疑



##### 项目搭建

`npm init -y`初始化项目，安装如下依赖：

```javascript
{
  "name": "great-react",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "webpack-dev-server"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@babel/core": "^7.11.4",
    "@babel/preset-env": "^7.11.0",
    "@babel/preset-react": "^7.10.4",
    "babel-loader": "^8.1.0",
    "clean-webpack-plugin": "^3.0.0",
    "html-webpack-plugin": "^4.3.0",
    "webpack": "^4.44.1",
    "webpack-cli": "^3.3.12",
    "webpack-dev-server": "^3.11.0"
  },
  "dependencies": {}
}

```

配置`webpack.config.js`：

```javascript
const path = require("path")
const HtmlWebpackPlugin = require("html-webpack-plugin")
const { CleanWebpackPlugin } = require("clean-webpack-plugin")

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve("dist"),
    filename: "bundle.js"
  },
  devtool: "inline-source-map",
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: "babel-loader"
      }
    ]
  },
  plugins: [
    // 在构建之前将dist文件夹清理掉
    // new CleanWebpackPlugin({
    //   cleanOnceBeforeBuildPatterns: ["./dist"]
    // }),
    // 指定HTML模板, 插件会将构建好的js文件自动插入到HTML文件中
    new HtmlWebpackPlugin({
      template: "./src/index.html"
    })
  ],
  devServer: {
    // 指定开发环境应用运行的根据目录
    contentBase: "./dist",
    // 指定控制台输出的信息
    stats: "errors-only",
    // 不启动压缩
    compress: false,
    host: "localhost",
    port: 5000
  }
}

```

新建文件react/index.js:

```javascript
import createElement from "./createElement";

export default {
  createElement,
}
```

新建文件react/createElement.js:

```javascript
export default function createElement(type, props, ...children) {
  return {
    type,
    props,
    children,
  }
}
```

同时配置.babelrc，调用改createElement.js：

```javascript
{
  "presets": [
    "@babel/preset-env",
    [
      "@babel/preset-react",{
        "pragma":"react.createElement"
      }
    ]
  ]
}
```

在react/index.js中写下jsx

```javascript
import react from "../react";
const root = document.getElementById('root')

const virtualDom = (
  <div className="container">
    <h1>你好 great React</h1>
    <h2 data-test="test123">H2 title</h2>
    <div>
      嵌套1 <div>嵌套 1.1</div>
    </div>
    {2 == 1 && <div>如果2和1相等渲染当前内容</div>}
    {2 == 2 && <div>2</div>}
    <button onClick={() => alert("你好!!!!!")}>点击我</button>
    <input type="text" value="13" />
  </div>
)

console.log(virtualDom)
```

在命令行运行`npm run start`,在浏览器控制台可以看到打印的虚拟dom：

![](C:\Users\Thomas东\AppData\Roaming\Typora\typora-user-images\1663226490649.png)

这里的虚拟dom和我们想要的虚拟dom还有一些差距，我们期待的文本节点是这样的：

```javascript
children: [
  {
    type: "text",
    props: {
      textContent: "React is great"
    }
  }
]
```

而且在jsx中表达式返回false时，是不会展示的，我们的虚拟dom却把它渲染成了false，接下来对createElement.js进行一些更改：

```javascript
export default function createElement(type, props, ...children) {
  const childElements = [].concat(...children).reduce((result, child) => {
    if (child !== false && child !== true && child !== null) {
      if (child instanceof Object) {
        result.push(child)
      } else {
        result.push(createElement("text", { textContent: child }))
      }
    }
    return result
  }, [])
  return {
    type,
    props: Object.assign({ children: childElements }, props),
    children: childElements
  }
}

```

这里先介绍下reduce方法的使用：

>  **`reduce()`** 方法对数组中的每个元素按序执行一个由您提供的 **reducer** 函数，每一次运行 **reducer** 会将先前元素的计算结果作为参数传入，最后将其结果汇总为单个返回值。 

> reduce接受两个参数，第一个是一个回调函数，第二个是一个初始值，回调函数中接受四个参数，分别是积累值、当前值、当前下标、当前数组。 
>
> 比如我们利用reduce查找数组的最大值：
>
> ```javascript
> [3, 5, 4, 3, 6, 2, 3, 4].reduce((a, i) => Math.max(a, i), -Infinity);
> ```
>
> 数组求和：
>
> ```javascript
> [3, 5, 4, 3, 6, 2, 3, 4].reduce((a, i) => a + i);
> ```

这里首先对传入的children通过concat()做了一个拷贝，再调用reduce方法对其中的虚拟dom进行处理，这里的result就是reduce函数返回的初始值，reduce的第二个参数将其初始化为一个空数组，child就是遍历的每一个child。首先判断child如果是布尔值，就直接返回，如果是对象的话，就将其放入result，如果不是就表明是一个文本了，这里在此调用createElement("text", { textContent: child })，并将结果放入result中。























