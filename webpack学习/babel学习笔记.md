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

  其中plugins来指定jsx、typescript、flow 等插件来解析对应的语法 ；soureType 指定否支持解析模块语法，有 module、script、unambiguous 3个取值，module 是解析 es module 语法，script 则不解析 es module 语法，当作脚本执行，unambiguous 则是根据内容是否有 import 和 export 来确定是否解析 es module 语法。 

- transform 阶段有 `@babel/traverse`，可以遍历 AST，并调用 visitor 函数修改 AST，修改 AST 自然涉及到 AST 的判断、创建、修改等，这时候就需要 `@babel/types` 了，当需要批量创建 AST 的时候可以使用 `@babel/template` 来简化 AST 创建逻辑。

  解析出来的AST在遍历和修改的过程中，可以使用`@babel/travrse`包，即

  ```javascript
  function traverse(parent, opts)
  ```

  parent 指定要遍历的 AST 节点，opts 指定 visitor 函数。babel 会在遍历 parent 对应的 AST 时调用相应的 visitor 函数。 

  visitor 对象的 value 是对象或者函数：

  - 如果 value 为函数，那么就相当于是 enter 时调用的函数。
  - 如果 value 为对象，则可以明确指定 enter 或者 exit 时的处理函数。

  ```javascript
  visitor: {
      Identifier (path, state) {},
      StringLiteral: {
          enter (path, state) {},
          exit (path, state) {}
      }
  }
  ```

  enter 时调用是在遍历当前节点的子节点前调用，exit 时调用是遍历完当前节点的子节点后调用。

  - path

    path是遍历过程中的路径，会保留上下文信息，有很多属性和方法：

    - path.node 指向当前 AST 节点
    - path.get、path.set 获取和设置当前节点属性的 path
    - path.parent 指向父级 AST 节点
    - path.getSibling、path.getNextSibling、path.getPrevSibling 获取兄弟节点
    - path.find 从当前节点向上查找节点
    - path.scope 获取当前节点的作用域信息
    - path.isXxx 判断当前节点是不是 xx 类型
    - path.assertXxx 判断当前节点是不是 xx 类型，不是则抛出异常
    - path.insertBefore、path.insertAfter 插入节点
    - path.replaceWith、path.replaceWithMultiple、replaceWithSourceString 替换节点
    - path.remove 删除节点
    - path.skip 跳过当前节点的子节点的遍历
    - path.stop 结束后续遍历

  - state

    state则是遍历过程中在不同节点之间传递数据的机制，插件会通过 state 传递 options 和 file 信息，我们也可以通过 state 存储一些遍历过程中的共享数据。 

- generate 阶段会把 AST 打印为目标代码字符串，同时生成 sourcemap，需要 `@babel/generate` 包

- 中途遇到错误想打印代码位置的时候，使用 `@babel/code-frame` 包

- babel 的整体功能通过 `@babel/core` 提供，基于上面的包完成 babel 整体的编译流程，并实现插件功能。

##### 实例： 函数插桩

通过 babel 能够自动在 console.log 等 api 中插入文件名和行列号的参数 。

这个例子也比较简单，根据babel编译流程，先根据code生成AST，再遍历AST，遍历完成后就根据AST生成对应字符。这个案例要在console中加入参数，就在遍历AST这个步骤中。首先使用`parser.parse`函数生成AST，再调用`traverse`函数进行遍历，

```javascript
const parser = require('@babel/parser');
const types = require('@babel/types');
const traverse = require('@babel/traverse').default;
const generate = require('@babel/generator').default;

const sourceCode = `
    console.log(1);

    function func() {
        console.info(2);
    }

    export default class Clazz {
        say() {
            console.debug(3);
        }
        render() {
            return <div>{console.error(4)}</div>
        }
    }
`;

const ast = parser.parse(sourceCode, {
    sourceType: 'unambiguous',
    plugins: ['jsx']
});

const targetCalleeName = ['log', 'info', 'error', 'debug'].map(item => `console.${item}`);
traverse(ast, {
    CallExpression(path, state) {
        const calleeName = generate(path.node.callee).code;
         if (targetCalleeName.includes(calleeName)) {
            const { line, column } = path.node.loc.start;
            path.node.arguments.unshift(types.stringLiteral(`filename: (${line}, ${column})`))
        }
    }
});

const { code, map } = generate(ast);
console.log(code);
```





























