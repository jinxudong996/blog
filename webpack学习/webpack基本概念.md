#### webpack学习笔记

1. ###### 基本概念

   入口：起点指示webpack应该使用那个模块，来作为构建其内部依赖图的开始，默认是./src/index.js，可以配置entry属性来指定入口。

   输出：告诉webpack在哪里输出所创建的bundle，以及如何命名这些文件，输出默认值是./dist/main.js，可以通过output来指定出口。

   loader：loader让webpack有能力去处理其他类型的文件，并将他们转化为有效模块，以供他们使用，以及被添加到依赖图中。

   plugin：loader用于转换某些类型的模块，而插件则可以用于执行范围更广的任务，包括：打包优化，资源管理，注入环境变量。使用插件可以通过require导入，再添加到plugins数组中。

2. ###### 入口起点

   ```JavaScript
   module.exports = {
     //注入单文件  
     entry: './path/to/my/entry/file.js', 
     //一次注入多个依赖文件
     entry: ['./src/file_1.js', './src/file_2.js'],
     output: {
       filename: 'bundle.js',
     },
   };
   
   ```

   

   ```JavaScript
   module.exports = {
     entry: {
       app: './src/app.js',
       adminApp: './src/adminApp.js',
     },
   }
   ```

   通过对象的语法，来配置具有更可扩展性的入口。

   入口对象的属性有：

   - dependOn：当前入口所依赖的入口，需要在入口被加载前加载

   - filename：指定输出的文件名称

   - import：启动时需=加载的模块

   - library：指定library选项，为当前的entry构建一个library

   - runtime：运行时chunk 的名字

   - publicPath：当该入口的输出文件在浏览器中被引用时，为他们指定一个公共url地址

     注意事项：

   - runtime和depenOn不应在同一个入口上同时使用
   - runtime不能指向已存在的入口名称
   - dependOn不能是循环引用

   

3. ###### 输出

   可以通过配置output选项，告诉webpack如何向硬盘写入编译文件。可以存在多个entry起点，但只能指定一个output配置。

4. ###### loader

   loader用于对模块的源代码进行转换。loader可以再加载文件时进行预处理，类似于其他构建工具中的任务，并提供了处理前端构建步骤的得力方式。

5. ###### plugin



垃圾  重写

1. 前置知识

   关于模块化的知识。

2. 

模块化概念

在一个复杂的应用程序里，按照一定的语法，遵循确定的规则将其拆分到几个互相独立的文件中，这些文件具有原子特性，在其内部完成共同的或者类似的逻辑，通过对外暴露一些数据或者调用方法，与外部完成整合。

在早期开发者通常通过函数的形式来模拟模块化的，将不同的功能封装成不同的函数

```
function fn1() {...}
function fn2() {...}
```

然而这种回导致合格函数混乱的互相调用，命名也有冲突的风险，并没有从根本上解决问题，只是将函数拆分为了更小的函数单元。

后来又有了对象模式，通过对象的属性和方法来模拟模块化

```
const module1 = {
	foo1:'bar',
	f11:function(){...}
}
```

这样module里的数据并不安全，因为当时还没有块级作用域的概念，任何人都可以通过`module1.foo1='dar'`来更改module1的内部状态。闭包的运用就出现了，通过立即执行函数，构造一个私有作用域，再通过闭包向外部暴露对应的接口。著名的jquery就是通过闭包将对外接口挂载到window上







先学习4.0

将js转译为低版本，需要用到babel-loader。首先安装babel-loader及其依赖：

```javascript
npm install babel-loader -D
npm install @babel/core @babel/preset-env @babel/plugin-transform-runtime -D
npm install @babel/runtime @babel/runtime-corejs3
```

在src目录下新建index.js文件，写上ES6语法  let name="nick"

新建webpack.config.js如下：

```javascript
module.exports = {
  mode: 'development',
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ["@babel/preset-env"],
            plugins: [
              [
                "@babel/plugin-transform-runtime",
                {
                    "corejs": 3
                }
              ]
            ]
          }
        },
        exclude: /node_modules/
      }
    ]
  }
}
```

运行npx webpack，就可以看到多了个dist目录及dist目录下的main.js

```javascript
(function(module, exports) {

eval("var name = 'nick';\n\n//# sourceURL=webpack:///./src/index.js?");

/***/ })
```

ES6已经被转译成了ES5语法。



在浏览器中查看页面

指定打包文件回带有hash值，就会导致每次生成的js文件名不一样，导入js就会有很麻烦，可以通过插件html-webpack-plugin插件来完成。新建public文件及index.html文件。

安装插件

```
npm install html-webpack-plugin -D 
```

在webpack.config.js中添加

```javascript
const HtmlWebpackPlugin = require('html-webpack-plugin');

plugins: [
    //数组 放着所有的webpack插件
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: 'index.html', //打包后的文件名
      minify: {
          removeAttributeQuotes: false, //是否删除属性的双引号
          collapseWhitespace: false, //是否折叠空白
      },
      // hash: true //是否加上hash，默认是 false
    })
  ]
```

运行npx webpack，此时就会看到dist目录下生成了main.js和index.html，在index.html中就可以看到main.js已经被引入html文件里

```html
<script type="text/javascript" src="main.js"></script></body>
```

这个插件很是强大的，不仅仅会引入js，还可以通过配置来生成指定的html。

在public文件下新建config.js

```javascript
module.exports = {
    dog: {
        template: {
            hair: 'red',
            name:'jack'
        }
    },
    cat: {
        template: {
            hair: 'black',
            name:'Jerry'
        }
    }
}
```

在webpack.config.js中添加：

```
const isDev = process.env.NODE_ENV === 'development';
const config = require('./public/config')[isDev ? 'dog' : 'cat'];

plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: 'index.html', //打包后的文件名
      config: config.template
    })
  ]
```

同时也在public/index.html文件中将title标签改为：

```html
<title><%= (htmlWebpackPlugin.options.config.name) %></title>
```

随后更改下打包命令，在package.json中添加：

```javascript
"scripts": {
    "dev": "cross-env NODE_ENV=development webpack",
    "build": "cross-env NODE_ENV=production webpack"
  },
```

运行 npm run dev  ,可以看到打包后的index.html中的title标签会跟着输入的命令变化。

```html
<title>jack</title>
```

在浏览器中显示

在webpack.config.js中添加webpack-dev-server配置：

```javascript
devServer: {
    port: '3000', //默认是8080
    quiet: false, //默认不启用
    inline: true, //默认开启 inline 模式，如果设置为false,开启 iframe 模式
    stats: "errors-only", //终端仅打印 error
    overlay: false, //默认不启用
    clientLogLevel: "silent", //日志等级
    compress: true //是否启用 gzip 压缩
  }
```

再更改下package.json中的script：

```
"scripts": {
    "dev": "cross-env NODE_ENV=development webpack-dev-server",
    "build": "cross-env NODE_ENV=production webpack"
  },
```

在命令行运行`npm run dev`，在浏览器中输入`localhost:30000`，即可看到public里的index.html内容。目前的代码都是经过编译后的，不容易调试，可以设置`devtool`将编译后的代码映射回源代码。

处理样式文件：

webpack不能直接处理css，需要借助loader。在webpack.config.js中的rules中添加：

```javascript
{
      test: /\.(le|c)ss$/,
      use: ['style-loader', 'css-loader', {
          loader: 'postcss-loader',
          options: {
              plugins: function () {
                  return [
                      require('autoprefixer')()
                  ]
              }
          }
        }, 'less-loader'],
        exclude: /node_modules/
    }
```

在src下面新建文件index.css:

```css
.color{
    color:red;
}
```

同时在index.js中引入 `import './index.less'`，运行`npm run dev`，即可看见页面颜色更改。



图片处理

使用url-loader进行处理，在rules中配置：

```
{
        test: /\.(png|jpg|gif|jpeg|webp|svg|eot|ttf|woff|woff2)$/,
        use: [
            {
                loader: 'url-loader',
                options: {
                    limit: 10240, //10K
                    esModule: false
                }
            }
        ],
        exclude: /node_modules/
    }
```

在index.css中引入图片：

```
.img{
    width:100px;
    height: 100px;
    border:1px solid red;
    background:url('../pka.png') 100% 100%;
}
```

在index.html中即可查看。



处理html中图片：

配置loader：

```
{
   test: /.html$/,
   use: 'html-withimg-loader'
},
```

在index.html中引入图片：

```
<img src="../pka.png" alt="">
```

