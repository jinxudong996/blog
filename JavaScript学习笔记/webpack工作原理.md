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



##### compiler和compilation

compiler和compilation这两个对象是webpack核心原理中最重要的概念，他们是理解webpack工作原理、loader和插件工作的基础。

- compiler对象：它的实例包含了完整的webpack配置，且全局只有一个compiler实例，因此它就像webpack的骨架或神经中枢。当插件被实例化时，就会收到一个compiler对象，通过这个对象可以访问webpack的内部环境。
- compilation对象：当webapck以开发模式运行时，每当检测到文件变化时，一个新的compilation对象就会被创建。这个对象包含了当前的模块资源、编译生成资源、变化的文件等信息。也就是说，所有构建过程中产生的构建数据都会被存储在该对象上，它也掌控着构建过程中的每一个环节。该对象还提供了很多事件回调供插件做扩展。

webpack的构建过程是通过compiler控制流程，通过compilation进行代码解析的。在开发插件时，我们可以从compiler对象中得到所有与webpack主环境的内容，包括事件钩子

compiler对象和compilation对象都继承自tapable库，该库暴露了所有和事件相关的发布订阅的方法。webpack中基于事件流的tapable库不仅能保证插件的有序性，还能使整个系统扩展性更好。



##### 手写一个简易的webpack





##### 手写loader





##### 手写插件



