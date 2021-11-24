const HtmlWebpackPlugin = require('html-webpack-plugin');
const isDev = process.env.NODE_ENV === 'development';
const config = require('./public/config')[isDev ? 'dog' : 'cat'];

module.exports = {
  mode: 'development',
  devtool: 'cheap-module-eval-source-map',
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        use: ['babel-loader'],
        exclude: /node_modules/ //排除 node_modules 目录
    },
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
    },{
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
    },{
         test: /.html$/,
         use: 'html-withimg-loader'
      },]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: 'index.html', //打包后的文件名
      config: config.template
    })
  ],
  // devServer: {
  //   port: '3000', //默认是8080
  //   quiet: false, //默认不启用
  //   inline: true, //默认开启 inline 模式，如果设置为false,开启 iframe 模式
  //   stats: "errors-only", //终端仅打印 error
  //   overlay: false, //默认不启用
  //   clientLogLevel: "silent", //日志等级
  //   compress: true //是否启用 gzip 压缩
  // }
}