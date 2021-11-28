webpackg工作原理



#### 输出

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



##### 源码阅读



##### 工作原理

![](https://user-images.githubusercontent.com/26785201/89747816-fe344280-daf2-11ea-820a-6a1a99e34f14.png)

- 首先webpack会读取项目中的配置文件`wenpack.config.js`，或者从shell语句中获取必要的参数，这是webapck从内部接受业务信息的方式。