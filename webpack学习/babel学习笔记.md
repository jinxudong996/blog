babel常用的就是将高版本js转译为低版本的js。

##### 使用方法

首先安装`webpack`和`babel`

```
"@babel/core": "^7.16.0",
"@babel/plugin-transform-runtime": "^7.16.4",
"@babel/preset-env": "^7.16.4",
"babel-loader": "^8.2.3",
"cross-env": "^7.0.3",
"webpack": "^5.64.2",
"webpack-cli": "^4.9.1",
```

在`webpack.config.js`中添加loader和定义入口和出口

```javascript
const path = require('path');
const isDev = process.env.NODE_ENV === 'development';

module.exports = {
  mode: isDev ? 'development' : 'production',
  // devtool: isDev ? 'source-map' : false,
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'), //必须是绝对路径
    filename: 'bundle.js',
  },
  module:{
    rules: [
      {
        test: /\.jsx?$/,
        use: ['babel-loader'],
        exclude: /node_modules/ //排除 node_modules 目录
      }
    ]
  }
  
}
```

再配一个`.babelrc`文件

```javascript
{
  "presets": [
    "@babel/preset-env"
  ],
  "plugins": [
    [
      "@babel/plugin-transform-runtime",
      {
        "corejs": 3
      }
    ]
  ]
}
```

在`package.json`中的`script`添加`"devBuild": "cross-env NODE_ENV=development webpack"`，在命令行运行`npm run devBuild`，既可以看到在根目录的dist目录下有一个打包完后的bundle.js文件，es6版本的js已经被转译成了es5。

##### 转译流程

babel 的编译流程分为三步：parse、transform、generate。

- parse阶段有`@babel/parser`，将源码转成AST

  ```javascript
  require("@babel/parser").parse("code", {
    sourceType: "module",
    plugins: [
      "jsx",
      "typescript"
    ]
  });
  ```

  

- transform 阶段有 `@babel/traverse`，可以遍历 AST，并调用 visitor 函数修改 AST，修改 AST 自然涉及到 AST 的判断、创建、修改等，这时候就需要 `@babel/types` 了，当需要批量创建 AST 的时候可以使用 `@babel/template` 来简化 AST 创建逻辑。

- generate 阶段会把 AST 打印为目标代码字符串，同时生成 sourcemap，需要 `@babel/generate` 包

- 中途遇到错误想打印代码位置的时候，使用 `@babel/code-frame` 包

- babel 的整体功能通过 `@babel/core` 提供，基于上面的包完成 babel 整体的编译流程，并实现插件功能。

##### 实例： 函数插桩

通过 babel 能够自动在 console.log 等 api 中插入文件名和行列号的参数 。

































