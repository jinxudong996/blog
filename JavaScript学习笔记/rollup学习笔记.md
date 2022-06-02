##### 简介

rollup 是一个 JavaScript 模块打包器，在功能上要完成的事和webpack性质一样，就是将小块代码编译成大块复杂的代码，例如 library 或应用程序。在平时开发应用程序时，我们基本上选择用webpack，相比之下，rollup.js更多是用于library打包，我们熟悉的vue、react、vuex、vue-router等都是用rollup进行打包的。

相比如webpack，webpack理念是“万物皆是模块”，具有着具有着极强的处理各类资源的能力。rollup给其定位只是一个模块打包工具，api简单，学习成本更低，也更加轻量，构建出的代码体积更小。对于由js编写的项目，比如组件库、前端框架，rollup更加适合的。

##### 初探

安装的话，也比较简单

```javascript
npm install rollup 
```

然后新建两个测试文件

```javascript
//foo.js
export default 'hello world!';

//bar.js
import foo from './foo.js';
export default function () {
  console.log(foo);
}
```

和webpack一样，需要一个配置文件，新建一个rollup.config.js

```javascript
export default {
  input: 'src/bar.js',
  output: {
    file: 'dist/bundle.js',
    format: 'cjs'
  }
};
```

output中的format可以指定不同的模块，比如：es、umd、esm、iife等。

在package.json中添加打包命令：

```javascript
"build":"rollup -c"
```

在命令行运行npm run build，既可以看到生出一个文件dist/bundle.js

```javascript
'use strict';

var foo = 'hello world!';

function bar () {
  console.log(foo);
}

module.exports = bar;
```

##### 常用插件