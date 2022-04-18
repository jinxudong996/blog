const path = require('path')

module.exports = {
  entry:'./index.js',
  output:{
    path:path.join(__dirname,'/dist'),
    filename:'index.js'
  },
  mode:'development'
}