webpackg工作原理



##### 输出

首先新建项目及安装依赖

```
npm init -y
npm install --save-dev webpack
npm install --save-dev webpack-cli
```

新建文件`src/index.js`和`src/hello.js`，index.js为默认入口文件：

```
const sayHello = require('./hello')
console.log(sayHello('nick'))
```

hello.js

```
module.exports = function(name) {
  return 'hello' + name
}
```

在命令行运行`npx webpack --mode=development`，打开编译文件`dist/main.js`：

```
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./src/hello.js":
/*!**********************!*\
  !*** ./src/hello.js ***!
  \**********************/
/***/ ((module) => {

eval("module.exports = function(name) {\r\n  return 'hello' + name\r\n}\n\n//# sourceURL=webpack://commonJS/./src/hello.js?");

/***/ }),

/***/ "./src/index.js":
/*!**********************!*\
  !*** ./src/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

eval("const sayHello = __webpack_require__(/*! ./hello */ \"./src/hello.js\")\r\nconsole.log(sayHello('nick'))\n\n//# sourceURL=webpack://commonJS/./src/index.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./src/index.js");
/******/ 	
/******/ })()
;
```

这里实际上外面包裹着一个IIFE(立即调用函数表达式)

```
(() => {
	var __webpack_modules__ = ({...})

	var __webpack_module_cache__ = {};

	function __webpack_require__(moduleId){...}

	var __webpack_exports__ = __webpack_require__("./src/index.js");
})()
```

核心代码就是这些

- webpack的打包结果就是一个IIFE，被称为webpackBootstrap
- webpack_modules是一个模块加载函数，里面定义了两个函数，也就是我们打包的文件：`./src/hello.js:(() => {})`和`./src/index.js:(() => {})`
- 定义了webpack_module_cache缓存对象
- webpack_require函数接受一个入口文件的路径作为参数，首先判断该参数是否在缓存对象中，如果在就返回缓存对象中的值；如果不在就先将参数写入缓存对象，随后创建一个新的`module`对象，并执行`webpack_modules`函数，实际上就是调用的是webpack_modules中定义的`./src/index.js:(() => {})`



##### 工作流程

![](https://user-images.githubusercontent.com/26785201/89747816-fe344280-daf2-11ea-820a-6a1a99e34f14.png)

- `entry-options启动`首先webpack会读取项目中的配置文件`wenpack.config.js`，或者从shell语句中获取必要的参数，这是webapck从内部接受业务信息的方式。
- `run 实例化` compiler用上一步得到的参数初始化Compiler对象，加载所配置的插件，执行对象的`run`方法开始执行编译
- `entry`确定入口：根据配置中entry找出所有的入口文件
- `make`编译模块：从入口文件出发，调用所有配置的`loader`对模块进行翻译，再递归找出该模块依赖的模块，
- `build module`完成模块编译：经过上面使用loader翻译完所有模块后，得到了每个模块被翻译后的最终内容以及他们之间的依赖关系。
- `seal`输出资源，根据入口和模块之间的依赖关系，组装成一个个包含多个模块的chunk，再把每个chunk转化成一个单独的文件加入到输出列表。
- `emit`输出完成：在确定好输出内容后，根据配置确定输出的路径和文件名，把文件内容写入到系统文件



##### 抽象语法树

> 在计算机科学中，抽象语法树（Abtract Syntax Tree,AST）是源码语法结构的一种抽象表示。它以树状的形式表现编程语言的语法结构，树上的每个节点都表示源码中的一种结构和

之所以说语法是抽象的，是因为这里的语法并不会表示出真实语法中出现的每一个细节。

webpack将文件转化为AST的目的就是方便开发者提取模块文件中的关键信息，这样一来，我们就可以知晓开发者到底写了什么东西，也就可以根据这些写出来的进行分析和扩展。

可以在`https://esprima.org/demo/parse.html#`这个网站上将代码解析成AST树。

```javascript
var answer = 6 * 7;
```

```javascript
{
  "type": "Program",
  "body": [
    {
      "type": "VariableDeclaration",
      "declarations": [
        {
          "type": "VariableDeclarator",
          "id": {
            "type": "Identifier",
            "name": "answer"
          },
          "init": {
            "type": "BinaryExpression",
            "operator": "*",
            "left": {
              "type": "Literal",
              "value": 6,
              "raw": "6"
            },
            "right": {
              "type": "Literal",
              "value": 7,
              "raw": "7"
            }
          }
        }
      ],
      "kind": "var"
    }
  ],
  "sourceType": "script"
}
```



##### compiler和compilation

compiler和compilation这两个对象是webpack核心原理中最重要的概念，他们是理解webpack工作原理、loader和插件工作的基础。

- compiler对象：它的实例包含了完整的webpack配置，且全局只有一个compiler实例，因此它就像webpack的骨架或神经中枢。当插件被实例化时，就会收到一个compiler对象，通过这个对象可以访问webpack的内部环境。
- compilation对象：当webapck以开发模式运行时，每当检测到文件变化时，一个新的compilation对象就会被创建。这个对象包含了当前的模块资源、编译生成资源、变化的文件等信息。也就是说，所有构建过程中产生的构建数据都会被存储在该对象上，它也掌控着构建过程中的每一个环节。该对象还提供了很多事件回调供插件做扩展。

webpack的构建过程是通过compiler控制流程，通过compilation进行代码解析的。在开发插件时，我们可以从compiler对象中得到所有与webpack主环境的内容，包括事件钩子

compiler对象和compilation对象都继承自tapable库，该库暴露了所有和事件相关的发布订阅的方法。webpack中基于事件流的tapable库不仅能保证插件的有序性，还能使整个系统扩展性更好。



##### 手写一个简易的webpack

###### 项目初始化

```
mkdir wpk
npm init -y
```

创建文件`src/index.js`和`src/greeting.js`为我们的即将打包的业务代码。

创建文件`lib/compiler.js`复测编译，构建module输出文件， `lib/index.js` 实例化Compiler类，将配置参数传入 ，`lib/parser.js`   负责解析功能。

创建配置文件`wpk.config.js`

```javascript
const path = require("path");
global.filename = path.join(__dirname,'./src')
module.exports = {
  entry: path.join(__dirname, "./src/index.js"),
  output: {
    path: path.join(__dirname, "./dist"),
    filename: "bundle.js",
  },
};
```

这里定义了入口和出口

同时我们的业务代码

`src/index.js`

```
import { greeting } from "./greeting.js";

document.write(greeting("天王盖地虎"));
```

`src/greeting.js`

```
export function greeting(name) {
  return "口令：" + name;
}
```

这个项目的所需要的依赖

`package.json`

```
"dependencies": {
    "@babel/preset-env": "^7.15.6",
    "babel-core": "^6.26.3",
    "babel-preset-env": "^1.7.0",
    "babel-traverse": "^6.26.0",
    "babylon": "^6.18.0"
  }
```

以及`.babelrc`

```
{
    "presets": [
        "@babel/preset-env"
    ]
}
```

###### 解析

项目初始化完成，首先完成`parse.js`的编写。

```javascript
const fs = require("fs");
const babylon = require("babylon");

module.exports = {

  getAST: (path) => {
    const source = fs.readFileSync(path, "utf-8");

    return babylon.parse(source,{
        sourceType:'module'
    })
  },
  
};
```

使用`babylon`，将文件解析成AST树。

>   Babylon 是 [Babel](https://github.com/babel/babel) 中使用的 JavaScript 解析器。  
>
> Babylon 根据 [Babel AST 的格式](https://github.com/babel/babylon/blob/master/ast/spec.md) 生成 AST 。它基于 [ESTree 规范](https://github.com/estree/estree)，具有以下差别（现在可以使用 `estree` 插件来取消掉这些差别）：
>
> - [文字](https://github.com/estree/estree/blob/master/es5.md#literal)符号会被替换为[字符串](https://github.com/babel/babylon/blob/master/ast/spec.md#stringliteral)，[数字](https://github.com/babel/babylon/blob/master/ast/spec.md#numericliteral)，[布尔](https://github.com/babel/babylon/blob/master/ast/spec.md#booleanliteral)，[Null](https://github.com/babel/babylon/blob/master/ast/spec.md#nullliteral)，[正则表达式](https://github.com/babel/babylon/blob/master/ast/spec.md#regexpliteral)
> - [属性](https://github.com/estree/estree/blob/master/es5.md#property)符号会被替换为 [ObjectProperty](https://github.com/babel/babylon/blob/master/ast/spec.md#objectproperty) 和 [ObjectMethod](https://github.com/babel/babylon/blob/master/ast/spec.md#objectmethod)
> - [方法定义](https://github.com/estree/estree/blob/master/es2015.md#methoddefinition)会被替换为[类方法](https://github.com/babel/babylon/blob/master/ast/spec.md#classmethod)
> - [指令](https://github.com/babel/babylon/blob/master/ast/spec.md#programs)和[语法块](https://github.com/babel/babylon/blob/master/ast/spec.md#blockstatement)的 `directives` 字段中包含额外的[指令](https://github.com/babel/babylon/blob/master/ast/spec.md#directive)和[指令字符集](https://github.com/babel/babylon/blob/master/ast/spec.md#directiveliteral)
> - [函数表达式](https://github.com/babel/babylon/blob/master/ast/spec.md#functionexpression)中的[类方法](https://github.com/babel/babylon/blob/master/ast/spec.md#classmethod)，[对象属性](https://github.com/babel/babylon/blob/master/ast/spec.md#objectproperty)和[对象方法](https://github.com/babel/babylon/blob/master/ast/spec.md#objectmethod)值属性的属性被强制/带入主方法节点。

新建测试文件，`src/test.js`

```
const path = require("path");
const { getAST} = require('./parser');

let ast = getAST(path.join(__dirname,'../src/index.js'))
console.log(ast)
```

在命令行即可看见生成的AST，有了生成的AST，可以使用`babel-traverse`解析出文件所有的依赖

```javascript
getDependencies: (ast) => {
    const dependencies = [];
    traverse(ast, {
      ImportDeclaration: ({ node }) => {
        dependencies.push(node.source.value);
      },
    });
    return dependencies;
  },
```

接下来将ES6代码转化为ES5

```
transform: (ast) => {
    const { code } = transformFromAst(ast, null, {
      presets: ["env"],
    });
    return code;
  },
```

`parser.js`中主要就三个方法：

- `getAST`： 将获取到的模块内容 解析成`AST`语法树
- `getDependencies`：遍历`AST`，将用到的依赖收集起来
- `transform`：把获得的`ES6`的`AST`转化成`ES5`

###### 编译

接下来开始编写`compiler.js`，创建`Compiler `类，完成以下功能

- 接收`wpk.config.js`配置参数，并初始化`entry`、`output`
- 开启编译`run`方法。处理构建模块、收集依赖、输出文件等。
- `buildModule`方法。主要用于构建模块（被`run`方法调用）
- `emitFiles`方法。输出文件（同样被`run`方法调用）

```javascript
const path = require("path");
const fs = require("fs");

module.exports = class Compiler {
  constructor(options) {
    const { entry, output } = options;
    this.entry = entry;
    this.output = output;
    this.modules = [];
  }
  // 开启编译
  run() {}
  // 构建模块相关
  buildModule(filename, isEntry) {
    // filename: 文件名称
    // isEntry: 是否是入口文件
  }
  // 输出文件
  emitFiles() {}
};
```

因为我们的入口文件是讲配置文件当做参数传入的，`new Compiler(options).run();`，在构造函数中就初始化`entry`、`output`和`modules`。

开始构建模块

```javascript
 run() {
    const entryModule = this.buildModule(this.entry, true);
    console.log(entryModule)
    this.modules.push(entryModule);
    this.modules.map((_module) => {
      _module.dependencies.map((dependency) => {
        this.modules.push(this.buildModule(dependency));
      });
    });
    console.log(this.modules);
  }

  buildModule(filename, isEntry) {
    let ast;
    if (isEntry) {
      ast = getAST(filename);
    } else {
      // const absolutePath = path.join(process.cwd(), './src',filename);
      const absolutePath = path.join(global.filename, filename);
      ast = getAST(absolutePath);
    }

    return {
      filename, // 文件名称
      dependencies: getDependencies(ast), // 依赖列表
      transformCode: transform(ast), // 转化后的代码
    };
  }
```

`buildModule`函数根据传入的文件名称，将文件解析成AST，返回构建的module，module实际上就是一个包含文件名、依赖列表和转化后的代码的对象。

在`run`函数中，将配置文件中定义的入口文件路径传入`buildModule`,随后将入口文件构建的module存入`modules`，开始递归遍历入口文件中所有的依赖，并将其构建成module。

有了所有的modules列表，将这些列表输出成一个文件。遍历modules列表，将所有的module转化成一个以文件名为名字的匿名函数，随后传入一个IIFE，这个IIFE完全仿照`webpack4`的输出文件

```javascript
emitFiles() {
    const outputPath = path.join(this.output.path, this.output.filename);
    let modules = "";
    this.modules.map((_module) => {
      modules += `'${_module.filename}' : function(require, module, exports) {${_module.transformCode}},`;
    });

    const bundle = `
      (function(modules) {
        function require(fileName) {
          const fn = modules[fileName];
          const module = { exports:{}};
          fn(require, module, module.exports)
          return module.exports
        }
        require('${this.entry}')
      })({${modules}})
    `;
    // console.log(bundle)
    fs.writeFileSync(outputPath, bundle, "utf-8");
  }
```

`webpack4`输出的IIFE

```
(function(modules) {
  // 已经加载过的模块
  var installedModules = {};

  // 模块加载函数
  function __webpack_require__(moduleId) {
    if(installedModules[moduleId]) {
      return installedModules[moduleId].exports;
    }
    var module = installedModules[moduleId] = {
      i: moduleId,
      l: false,
      exports: {}
    };
    modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
    module.l = true;
    return module.exports;
  }
  __webpack_require__(0);
})([
/* 0 module */
(function(module, exports, __webpack_require__) {
  ...
}),
/* 1 module */
(function(module, exports, __webpack_require__) {
  ...
}),
/* n module */
(function(module, exports, __webpack_require__) {
  ...
})]);
```

- `webpack` 将所有模块(可以简单理解成文件)包裹于一个函数中，并传入默认参数，将所有模块放入一个数组中，取名为 `modules`，并通过数组的下标来作为 `moduleId`。
- 将 `modules` 传入一个自执行函数中，自执行函数中包含一个 `installedModules` 已经加载过的模块和一个模块加载函数，最后加载入口模块并返回。
- `__webpack_require__` 模块加载，先判断 `installedModules` 是否已加载，加载过了就直接返回 `exports` 数据，没有加载过该模块就通过 `modules[moduleId].call(module.exports, module, module.exports, __webpack_require__)` 执行模块并且将 `module.exports` 给返回。

这个时候打开`dist/bundle.js`既可以看到打包完成的文件，新建`dist/index.html`，既可以看到页面输出的内容。

目前简易的webpack已经编写完成，美中不足的是正宗的webpack运行命令都是`webpack`，我们这里也来改进一下下。在`package.json`中添加

```javascript
"bin": {
    "wpk": "lib/index.js" //入口文件
  },
```

在根目录下运行`npm link`将指定文件链接到全局，直接`wpk`既可以完成打包。如果想使用`npm run build`，也可以在`package.json`中的`script`中添加`"build": "wpk"`即可。

##### 手写loader





##### 手写插件



