 `webpack` 是一个现代 `JavaScript` 应用程序的静态模块打包器，当 `webpack` 处理应用程序时，会递归构建一个依赖关系图，其中包含应用程序需要的每个模块，然后将这些模块打包成一个或多个 `bundle`。 

主要有四个核心概念：

- entry: 入口
- output: 输出
- loader: 模块转换器，用于把模块原内容按照需求转换成新内容
- 插件(plugins): 扩展插件，在webpack构建流程中的特定时机注入扩展逻辑来改变构建结果或做你想要做的事情

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

在` webpack.config.js `添加`rules`:

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



##### 图片处理

