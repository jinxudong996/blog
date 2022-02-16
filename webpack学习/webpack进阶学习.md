webpack构建速度和体积优化策略



##### 速度分析

```javascript
const SpeedMeasurePlugin = require('speed-measure-webpack-plugin')

const smp = new SpeedMeasurePlugin()

const webpackConfig = smp.wrap({
	plugins:[...]
})
```

用`smp.wrap()`将配置对象包裹起来，运行打包命令，即可在命令行查看loader和插件的耗时

##### 体积分析

```javascript
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

module.exports = {
	plugins:[
		new BundleAnalyzerPlugin()
	]
}
```

运行打包命令后会开启一个8888端口的网页，网页上展示了项目的情况，包含每个大文件的体积大小，可以据此详细的找到对应的文件，然后做一些优化，譬如按需加载啊，懒加载啊等。

##### 多进程/多实例构建

通过thread-loader解析资源

- 原理：
  - 每次 webpack 解析一个模块，thread-loader 会将它及它的依赖分配给 worker 线程中
  - 把这个 loader 放置在其他 loader 之前， 放置在这个 loader 之后的 loader 就会在一个单独的 worker 池(worker pool)中运行
- 在 worker 池(worker pool)中运行的 loader 是受到限制的。例如：
  - 这些 loader 不能产生新的文件。
  - 这些 loader 不能使用定制的 loader API（也就是说，通过插件）。
  - 这些 loader 无法获取 webpack 的选项设置。
- 每个 worker 都是一个单独的有 600ms 限制的 node.js 进程。同时跨进程的数据交换也会被限制。

```javascript
module.exports = {
  module: {
    rules: [
      {
        test: /\.js$/,
        include: path.resolve('src'),
        use: [
          'thread-loader',
          // your expensive loader (e.g babel-loader)
        ],
      },
    ],
  },
};
```

还可以做一些详细的配置：

```javascript
use: [
  {
    loader: 'thread-loader',
    // loaders with equal options will share worker pools
    options: {
      // the number of spawned workers, defaults to (number of cpus - 1) or
      // fallback to 1 when require('os').cpus() is undefined
      workers: 2,

      // number of jobs a worker processes in parallel
      // defaults to 20
      workerParallelJobs: 50,

      // additional node.js arguments
      workerNodeArgs: ['--max-old-space-size=1024'],

      // Allow to respawn a dead worker pool
      // respawning slows down the entire compilation
      // and should be set to false for development
      poolRespawn: false,

      // timeout for killing the worker processes when idle
      // defaults to 500 (ms)
      // can be set to Infinity for watching builds to keep workers alive
      poolTimeout: 2000,

      // number of jobs the poll distributes to the workers
      // defaults to 200
      // decrease of less efficient but more fair distribution
      poolParallelJobs: 50,

      // name of the pool
      // can be used to create different pools with elsewise identical options
      name: 'my-pool',
    },
  },
  // your expensive loader (e.g babel-loader)
];
```

详细可以查看[官方文档](https://webpack.js.org/loaders/thread-loader/)

##### 并行压缩

也可以使用多进程/多实例并行压缩代码，来提升构建速度。

```javascript
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin()],
  },
};
```

##### 分包

将一些基础包通过cdn引入，不打入bundle。 如react开发时，每个组件都需要引入react和react-dom，我们打包时这两个基础库体积较大，导致构建出来的包提交变大~这个时候，我们可以考虑将react和react-dom在html中用CDN引入 。

```javascript
const HtmlWebpackExternalsPlugin = require('html-webpack-externals-plugin');

module.exports = {
    new HtmlWebpackExternalsPlugin({
        externals: [
            {
                module: 'react',
                entry: 'https://11.url.cn/now/lib/16.2.0/react.min.js',
                global: 'React'
            },
            {
                module: 'react-dom',
                entry: 'https://11.url.cn/now/lib/16.2.0/react-dom.min.js',
                global: 'ReactDOM'
            }
        ]
    })
};
```

##### 利用缓存提升二次构建速度

缓存思路：

babel-loader开启缓存

terser-webpack-plugin开启缓存

使用cache-loader或者hard-source-webpack-plugin

```javascript
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin(
    	{
            parallerl:true,
        	cache:true,//开启缓存
        }
    )],
  },
};
```

##### 缩小构建目标

尽可能的少构建模块，比如babel-loader不解析node_modules，

```javascript
module.exports = {
	rules:{
		{
        test: /\.jsx?$/,
        use: ['babel-loader'],
        exclude: /node_modules/ //排除 node_modules 目录
      }
	}
}
```

优化resolve.modules配置，减少模块搜索层级

```javascript
module.exports = {
	resolve:{
		modules:[path.resolve(__dirname,'node_modules')],
        extensions:['.js'],
        mainFields:['main'],
	}
}
```



##### 图片压缩

Imagemin的压缩原理：

- pngquant：是一款PNG压缩器，通过将图像转换为具有alpha通道（通常比24/32位PNG文件小60%—80%）的更高效的8位PNG格式，可显著减少文件代销
- pngcrush：其目的是通过尝试不同的压缩级别和PNG过滤方法来降低PNG IDAT数据流的大小

使用image-webpack-loader，详细内容可看[文档](https://github.com/tcoopman/image-webpack-loader)

```javascript
rules: [{
  test: /\.(gif|png|jpe?g|svg)$/i,
  use: [
    'file-loader',
    {
      loader: 'image-webpack-loader',
      options: {
        mozjpeg: {
          progressive: true,
        },
        // optipng.enabled: false will disable optipng
        optipng: {
          enabled: false,
        },
        pngquant: {
          quality: [0.65, 0.90],
          speed: 4
        },
        gifsicle: {
          interlaced: false,
        },
        // the webp option will enable WEBP
        webp: {
          quality: 75
        }
      }
    },
  ],
}]
```



##### TreeShaking擦除无用的css

一个模块可能有多个方法，只要其中一个方法被使用到了，则整个文件都会被打到bundle里面去，tree shaking就是只把有用的方法打入bundle，没用的方法会在uglify阶段被擦除掉。

通过purgecss-webpack-plugin和min-css-extract-plugin来完成擦除无用的css。[官方文档](https://github.com/FullHuman/purgecss/tree/master/packages/purgecss-webpack-plugin)

```javascript
const path = require('path')
const glob = require('glob')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const PurgeCSSPlugin = require('purgecss-webpack-plugin')

const PATHS = {
  src: path.join(__dirname, 'src')
}

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist')
  },
  optimization: {
    splitChunks: {
      cacheGroups: {
        styles: {
          name: 'styles',
          test: /\.css$/,
          chunks: 'all',
          enforce: true
        }
      }
    }
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader"
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].css",
    }),
    new PurgeCSSPlugin({
      paths: glob.sync(`${PATHS.src}/**/*`,  { nodir: true }),
    }),
  ]
}
```

