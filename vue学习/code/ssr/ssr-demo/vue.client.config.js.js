const VueSSRClientPlugin = require('vue-server-renderer/client-plugin')

module.exports = {
  configureWebpack: () => ({
    entry: `./src/client-entry.js`,
    devtool: 'source-map',
    target: 'web',
    plugins: [
      new VueSSRClientPlugin()
    ]
  }),
  chainWebpack: config => {
    // 去除所有关于客户端生成的html配置，因为已经交给后端生成
    config.plugins.delete('html');
    config.plugins.delete('preload');
    config.plugins.delete('prefetch');
  }
};