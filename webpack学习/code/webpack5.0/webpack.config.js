const path = require('path');
const isDev = process.env.NODE_ENV === 'development';
const HtmlWebpackPlugin = require('html-webpack-plugin');
const config = require('./public/config')[isDev ? 'dog' : 'cat'];

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
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: 'index.html', //打包后的文件名
      config: config.template
    })
  ],
}