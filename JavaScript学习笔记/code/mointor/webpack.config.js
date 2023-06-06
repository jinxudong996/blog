const path = require('path');

  module.exports = {
    entry: './src/index.js',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: 'mointor.js',
      library: {
        name: "mointor",
        type: "umd"
      },
    },
  };