 `webpack` 是一个现代 `JavaScript` 应用程序的静态模块打包器，当 `webpack` 处理应用程序时，会递归构建一个依赖关系图，其中包含应用程序需要的每个模块，然后将这些模块打包成一个或多个 `bundle`。 

主要有四个核心概念：

- 入口：起点指示webpack应该使用那个模块，来作为构建其内部依赖图的开始，默认是./src/index.js，可以配置entry属性来指定入口。


- 输出：告诉webpack在哪里输出所创建的bundle，以及如何命名这些文件，输出默认值是./dist/main.js，可以通过output来指定出口。


- loader：loader让webpack有能力去处理其他类型的文件，并将他们转化为有效模块，以供他们使用，以及被添加到依赖图中。


- plugin：loader用于转换某些类型的模块，而插件则可以用于执行范围更广的任务，包括：打包优化，资源管理，注入环境变量。使用插件可以通过require导入，再添加到plugins数组中。

#### 项目初始化

新建文档`webpack5.0`，运行`npm init -y`初始化项目，安装`webpack`、`webapck-cli`：

```
npm install webpack webpack-cli -D
```

安装的版本为：

```
"webpack": "^5.64.2",
"webpack-cli": "^4.9.1"
```

新建一个`src/idnex.js`文件：

```javascript
class Animal {
    constructor(name) {
        this.name = name;
    }
    getName() {
        return this.name;
    }
}

const dog = new Animal('dog');
```

在命令行运行` npx webpack --mode=development `可以看到在根目录下新增了一个`dist/main.js`文件。这里使用的都是webapck的默认配置，在 `node_modules/webpack/lib/WebpackOptionsDefaulter.js`里详细看一下，在`node_modules/webpack/lib/config/defaults.js`

```
F(output, "path", () => path.join(process.cwd(), "dist"));
```

我们可以自己设置入口与出口配置，自定义打包的入口文件与出口文件：

新建` webpack.config.js `文件：

```javascript
const path = require('path');

module.exports = {
  entry:'./src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'), //必须是绝对路径
    filename: 'bundle.js',
  }
}
```

一般我们在项目打包就是`npm run build`，现在需要在`package.json`的script中添加配置：

```
"build": "cross-env NODE_ENV=production webpack",
"devBuild": "cross-env NODE_ENV=development webpack"
```

完整的`webpack.config.js`如下：

```
const path = require('path');
const isDev = process.env.NODE_ENV === 'development';

module.exports = {
  mode:isDev ? 'development' : 'production',
  devtool: isDev ? 'source-map' : false,
  entry:'./src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'), //必须是绝对路径
    filename: 'bundle.js',
  }
}
```

现在运行`npm run build`或者`npm run devBuild`即可完成打包，即在`dist/build.js`下生成了打包文件。

项目基础已经搭建完成，接下来做一些有意思的小案例。

#### 基本案例

##### 将js转译为低版本

前面打包的代码还是ES6的代码，要将ES6代码转译为ES5代码，需要使用`babel-loader`和其依赖。

```
npm install babel-loader -D
npm install @babel/core @babel/preset-env @babel/plugin-transform-runtime -D
npm install @babel/runtime @babel/runtime-corejs3
```

loader有两个属性：

1. `test` 属性，识别出哪些文件会被转换。
2. `use` 属性，定义出在进行转换时，应该使用哪个 loader。

loader使用有两种方式：

- 配置方式（推荐）：在`webpack.config.js`文件中指定loader
- 内联方式：在每个`import`语句中显示指定loader



在` webpack.config.js `添加`module.rules`:

```javascript
rules: [
	{
        test: /\.jsx?$/,
        use: ['babel-loader'],
        exclude: /node_modules/ //排除 node_modules 目录
     }
]
```

同时在根目录下配置一个`.babelrc`文件：

```javascript
{
    "presets": ["@babel/preset-env"],
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

在命令行运行`npm run devBuild`，就可以看到ES6代码已经被转译了。



##### 在浏览器中查看页面

可以根据配置文件动态展示页面内容。

安装所需插件：

```
"webpack-dev-server": "^4.5.0"
"html-webpack-plugin": "^5.5.0",
```

先在根目录下新建一个`public/index.html`和`public/config.js`文件：

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

```html
<!DOCTYPE html>
<html>
<head>
	<title><%= (htmlWebpackPlugin.options.config.name) %></title>
	<meta charset="utf-8">
</head>
<body>
    <div><%= (htmlWebpackPlugin.options.config.hair) %></div>
    <div class="color">hello world</div>
    
</script>
</body>
</html>
```

在`package.json`中的script添加：

```
"dev": "cross-env NODE_ENV=development webpack-dev-server"
```

在`webpack.config.js`添加插件：

```
const HtmlWebpackPlugin = require('html-webpack-plugin');
...
plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: 'index.html', //打包后的文件名
      config: config.template
    })
  ],
```

运行`npm run dev`，在http://localhost:8080/中即可看到dog模板中的内容。

##### 处理样式文件

webpack处理css需要借助loader。首先安装依赖：

```
npm install style-loader less-loader css-loader postcss-loader autoprefixer less -D
```

在relus中添加：

```
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

新建`src/index.css`：

```
.color{
    color:red;
}
```

这里改了半天，`webpack5.0`和高版本loader不兼容，降级之后打包成功。

```
"autoprefixer": "^9.0.0",
"postcss-loader": "^3.0.0",
//https://github.com/laravel-mix/laravel-mix/issues/2471
//https://stackoverflow.com/questions/64057023/error-postcss-plugin-autoprefixer-requires-postcss-8-update-postcss-or-downgra
```

已经可以看到页面的hello world变成了红色。

##### 图片处理

处理本地资源可以使用`url-loader`。

在rules配置loader：

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

在`index.css`中引入图片：

```
.img{
    width:100vh;
    height: 100px;
    border:1px solid red;
    background:url('../pka1.png');
}
```

既可以成功在页面上看到所引入的图片了。

##### 静态资源拷贝

当需要使用已有的本地文件但不需要`webpack`编译，除了手动复制到构建目录（dist），还可以是使用[copy-webpack-plugin](https://webpack.js.org/plugins/copy-webpack-plugin/)插件。

该插件有两个参数：

- patterns, {Array<String|Object>} ,为插件指定文件相关模式。
  - [ ] from 复制文件的路径
  - [ ] to  输出路径
  - [ ] content  决定如何解释from的路径
  - [ ] toType  确定to的选项  dir-目录，file-文件，template-模板
  - [ ] globOptions， 允许配置插件使用的 glob 模式匹配库 
- options, {Object} , 指定插件选项 

新建文件`public/js/color.js``public/js/filter.js`和：

```
console.log('这是待引入的js文件')
```

```
console.log('这是要过滤的js文件')
```

在`webpack.config.js`中添加配置：

```
const CopyWebpackPlugin = require('copy-webpack-plugin');

...
//plugins中添加
new CopyWebpackPlugin({
    patterns:[
       {
          from: 'public/js/*.js',
          to: path.resolve(__dirname, 'dist', 'js'),
          toType:'dir',
          globOptions:{
            ignore: ["**/filter.*"],
          }
        },
})

```

运行`npm run devBuild`，即可看见在dist目录下有一个拷贝的js文件夹，里面只有`color.js`。



##### 单独打包css文件

如果需要单独打包css文件，可以用到` mini-css-extract-plugin `插件。

> 这个插件将 CSS 提取到单独的文件中。它为每个包含 CSS 的 JS 文件创建一个 CSS 文件。它支持按需加载 CSS 和 SourceMap。
>
> 它建立在新的 webpack v5 功能之上，并且需要 webpack 5 才能工作。

常用参数：

- [ ] filename 确定每个输出css文件的名称
- [ ] chunkFilename  确定非条目块的名称

首先安装依赖：` npm install mini-css-extract-plugin -D `，

更改`webapck.config.js`：

```
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

。。。
new MiniCssExtractPlugin({
    filename: 'css/[name].css'
})
```

并且使用`MiniCssExtractPlugin.loader`替换`style-loader`。

运行`nom run devBuild`，既可以看见dist目录下新增了一个css文件。



##### 按需加载

>  很多时候我们不需要一次性加载所有的JS文件，而应该在不同阶段去加载所需要的代码。`webpack`内置了强大的分割代码的功能可以实现按需加载。 

比如vue文档中提到可以使用路由懒加载提升性能：

>  当打包构建应用时，JavaScript 包会变得非常大，影响页面加载。如果我们能把不同路由对应的组件分割成不同的代码块，然后当路由被访问的时候才加载对应组件，这样就更加高效了。 

```
const Foo = () => import(/* webpackChunkName: "group-foo" */ './Foo.vue')
const Bar = () => import(/* webpackChunkName: "group-foo" */ './Bar.vue')
const Baz = () => import(/* webpackChunkName: "group-foo" */ './Baz.vue')
```



##### 热更新

配置devServer中的hot:true，随后在`webpack.config.js`中配置：

```
const webpack = require('webpack');
...//在plugins中添加插件
new webpack.HotModuleReplacementPlugin(), //热更新插件
```

[代码地址](https://github.com/jinxudong996/blog/tree/main/webpack%E5%AD%A6%E4%B9%A0/code/webpack5.0)









