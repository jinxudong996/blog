const isDev = process.env.NODE_ENV === 'development';
const config = require('./public/config')[isDev ? 'dog' : 'cat'];

const path = require('path');
const webpack = require('webpack');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');


module.exports = {
  mode:isDev ? 'development' : 'production',
  devtool: isDev ? 'eval-source-map' : false,
  entry:'./src/index.js',
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
      },{
        test: /\.(le|c)ss$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader', {
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
      }

    ]
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(), //热更新插件
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: 'index.html', //打包后的文件名
      config: config.template
    }),
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
      ]
    }),
    new MiniCssExtractPlugin({
      filename: 'css/[name].css'
    })
  ],
  devServer: {
    port: '3003', //默认是8080
    hot:true,
    // quiet: false, //默认不启用
    // inline: true, //默认开启 inline 模式，如果设置为false,开启 iframe 模式
    // // stats: "errors-only", //终端仅打印 error
    // // overlay: false, //默认不启用
    // // clientLogLevel: "silent", //日志等级
    // compress: true //是否启用 gzip 压缩
  }
}