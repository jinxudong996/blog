高级前端必会之babel全知全解

`babel` 是一个通用的多功能JavaScript编译器，也被称为源码到源码的编译器（转换编译器）。它主要用于将ECMAScript 2015+代码转换为向后兼容的JavaScript版本，让开发者能够使用最新的JavaScript特性，而无需担心兼容性问题。 

而`babyLon` 最初是Babel的解析器（parser），它负责将JavaScript代码解析成抽象语法树（AST），是Babel进行代码转换的基础工具之一。后来Babylon移入Babel的monorepo，更名为`@babel/parser`，成为Babel核心解析模块的一部分。 

##### 解析流程

首先安装`@babel/parser`，然后再`package.json`中指定`"type": "module"`

运行代码

```js
import * as parser from "@babel/parser";

const code = `function square(n) {
  return n * n;
}`;

try {
  const ast = parser.parse(code, { sourceType: "module" });
  console.log(ast);
} catch (e) {
  console.error("解析失败:", e.message);
}
输出
Node {
  type: 'File',
  start: 0,
  end: 38,
  loc: SourceLocation {
    start: Position { line: 1, column: 0, index: 0 },
    end: Position { line: 3, column: 1, index: 38 }, 
    filename: undefined,
    identifierName: undefined
  },
  errors: [],
  program: Node {
    。。。
  },
  comments: []
}
```

输出的就是我们的`AST抽象语法树`

`babel`解析流程一般是这样：

 ![img](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ee9eaa1f265c4c49ad156f2c691748d9~tplv-k3u1fbpfcp-jj-mark:1890:0:0:0:q75.awebp) 

###### parse

 parse 阶段的目的是把源码字符串转换成机器能够理解的 AST，这个过程分为词法分析、语法分析。 其中词法分析阶段就是把字符串形式的代码转换为令牌(tokens)流，

比如` n * n; `这样一行代码，

```js
[
  { type: { ... }, value: "n", start: 0, end: 1, loc: { ... } },
  { type: { ... }, value: "*", start: 2, end: 3, loc: { ... } },
  { type: { ... }, value: "n", start: 4, end: 5, loc: { ... } },
  ...
]
```

 每一个 `type` 有一组属性来描述该令牌： 

```js
{
  type: {
    label: 'name',
    keyword: undefined,
    beforeExpr: false,
    startsExpr: true,
    rightAssociative: false,
    isLoop: false,
    isAssign: false,
    prefix: false,
    postfix: false,
    binop: null,
    updateContext: null
  },
  ...
}
```

 和 AST 节点一样它们也有 `start`，`end`，`loc` 属性。 

语法分析阶段会把一个令牌流转换成抽象语法树的形式，这个阶段会使用令牌中的信息把他妈呢转成一个AST的表述结构，这样更易于后续的操作。

这个阶段主要使用`@babel/parser`这个包来解析我们的源码，生成`AST`

```js
const  parser = require('@babel/parser');

const ast = parser.parse("代码", {
    sourceType: 'unambiguous',
    plugins: ['jsx']
});
```

- `plugins`： 指定jsx、typescript、flow 等插件来解析对应的语法
- `sourceType`： 指定是否支持解析模块语法，有 module、script、unambiguous 3个取值：
  - module：解析 es module 语法
  - script：不解析 es module 语法
  - unambiguous：根据内容是否有 import 和 export 来自动设置 module 还是 script



###### transform 

 transform 阶段是对 parse 生成的 AST 的处理，会进行 AST 的遍历，遍历的过程中处理到不同的 AST 节点会调用注册的相应的 visitor 函数，visitor 函数里可以对 AST 节点进行增删改，返回新的 AST（可以指定是否继续遍历新生成的 AST）。 

 parse 出的 AST 由 `@babel/traverse` 来遍历和修改， `@babel/traverse`  包提供了 `traverse`方法，这个方法常用的就接收两个参数`parent`和`opts`， `parent` 指定要遍历的` AST` 节点，`opts` 指定 `visitor` 函数。`babel `会在遍历 `parent` 对应的 `AST` 时调用相应的 `visitor` 函数。 `visitor` 是指定对什么 `AST` 做什么处理的函数，`babel` 会在遍历到对应的 `AST` 时回调它们。而且可以指定刚开始遍历（enter）和遍历结束后（exit）两个阶段的回调函数。

每个` visitor  `都有path和state两个参数，其中path对象就记录了遍历`AST`节点的关联关系，有这样的节点：

- path.node 指向当前 AST 节点
- path.parent 指向父级 AST 节点
- path.getSibling、path.getNextSibling、path.getPrevSibling 获取兄弟节点
- path.find 从当前节点向上查找节点
- path.get、path.set 获取 / 设置属性的 path
- path.scope 获取当前节点的作用域信息
- path.isXxx 判断当前节点是不是 xx 类型
- path.assertXxx 判断当前节点是不是 xx 类型，不是则抛出异常

- path.insertBefore、path.insertAfter 插入节点
- path.replaceWith、path.replaceWithMultiple、replaceWithSourceString 替换节点
- path.remove 删除节点
- path.skip 跳过当前节点的子节点的遍历
- path.stop 结束后续遍历

第二个参数state 遍历过程中在不同节点之间传递数据的机制，插件会通过 state 传递 options 和 file 信息，我们也可以通过 state 存储一些遍历过程中的共享数据。 

在遍历 AST 的过程中需要创建一些 AST 和判断 AST 的类型，这时候就需要 `@babel/types` 包。 



###### generate 

 generate 阶段会把 AST 打印成目标代码字符串，并且会生成 sourcemap。不同的 AST 对应的不同结构的字符串。 

AST 转换完之后就要打印成目标代码字符串，通过 `@babel/generator` 包的 generate api

```javascript
javascript复制代码function (ast: Object, opts: Object, code: string): {code, map} 
```

第一个参数是要打印的 AST。

第二个参数是 options，指定打印的一些细节，比如通过 comments 指定是否包含注释，通过 minified 指定是否包含空白字符。

第三个参数当多个文件合并打印的时候需要用到，这部分直接看[文档](https://link.juejin.cn/?target=https%3A%2F%2Fbabeljs.io%2Fdocs%2Fen%2Fbabel-generator)即可，基本用不到。

options 中常用的是 sourceMaps，开启了这个选项才会生成 sourcemap。

```javascript
javascript复制代码import generate from "@babel/generator";

const { code, map } = generate(ast, { sourceMaps: true })
```



##### 常见的AST

接下来学习下常见的`AST`节点

###### Literal

`Literal`就是字面量的意思，对应`JavaScript`中基本数据类型。

常见的有` StringLiteral `字符串字面量，`NumbericLiteral`数字字面量，`BooleanLiteral`布尔字面量，`RegExoLiteral`正则表达式字面量

###### Identifier

 `Identifer` 是标识符的意思，变量名、属性名、参数名等各种声明和引用的名字，都是`Identifer`。 

###### Statement

`statement` 是语句，它是可以独立执行的单位，比如 break、continue、debugger、return 或者 if 语句、while 语句、for 语句，还有声明语句，表达式语句等。我们写的每一条可以独立执行的代码都是语句。

语句末尾一般会加一个分号分隔，或者用换行分隔。

###### Declaration

 声明语句是一种特殊的语句，它执行的逻辑是在作用域内声明一个变量、函数、class、import、export 等。  声明语句用于定义变量，这也是代码中一个基础组成部分。 

###### Expression

 expression 是表达式，特点是执行完以后有返回值，这是和语句 (statement) 的区别。 

###### Class

class 的语法也有专门的 AST 节点来表示。整个 class 的内容是 ClassBody，属性是 ClassProperty，方法是ClassMethod（通过 kind 属性来区分是 constructor 还是 method）。

###### 公共属性

每种 AST 都有自己的属性，但是它们也有一些公共的属性：

- `type`： AST 节点的类型
- `start、end、loc`：start 和 end 代表该节点在源码中的开始和结束下标。而 loc 属性是一个对象，有 line 和 column 属性分别记录开始和结束的行列号。
- `leadingComments、innerComments、trailingComments`： 表示开始的注释、中间的注释、结尾的注释，每个 AST 节点中都可能存在注释，而且可能在开始、中间、结束这三种位置，想拿到某个 AST 的注释就通过这三个属性。

















##### 案例

###### 自动国际化





###### 自动生成API







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

  其中plugins来指定jsx、typescript、flow 等插件来解析对应的语法 ；soureType 指定是否支持解析模块语法，有 module、script、unambiguous 3个取值，module 是解析 es module 语法，script 则不解析 es module 语法，当作脚本执行，unambiguous 则是根据内容是否有 import 和 export 来确定是否解析 es module 语法。 

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





























