const path = require('path');

module.exports = {
  // entry: './src/index.js',
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'distT'),
    filename: 'mointor.js',
    globalObject: 'this',
    library: {
      name: "mointor",
      type: "umd"
    },
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        use: ['babel-loader'],
        exclude: /node_modules/ //排除 node_modules 目录
      }
    ]
  }

};