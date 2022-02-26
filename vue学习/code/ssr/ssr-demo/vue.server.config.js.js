const nodeExternals = require("webpack-node-externals");
const VueSSRServerPlugin = require('vue-server-renderer/server-plugin')

module.exports = {
  css: {
    extract: false // 不提取 CSS
  },
  configureWebpack: () => ({
    entry: `./src/server-entry.js`, // 服务器入口文件
    devtool: 'source-map',
    target: 'node', // 构建目标为nodejs环境
    output: {
      libraryTarget: 'commonjs2' // 构建目标加载模式 commonjs
    },
    // 跳过 node_mdoules，运行时会自动加载，不需要编译
    externals: nodeExternals({
      allowlist: [/\.css$/] // 允许css文件，方便css module
    }),
    optimization: {
      splitChunks: false // 关闭代码切割
    },
    plugins: [
      new VueSSRServerPlugin()
    ]
  })
};