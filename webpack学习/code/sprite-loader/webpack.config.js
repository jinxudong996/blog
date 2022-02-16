const path = require('path')
const Myplugin = require('./plugins/my-plugins')

module.exports = {
    entry:'./src/index.js',
    output:{
        path:path.join(__dirname,'dist-plugin'),
        filename:'index.js'
    },
    plugins:[new Myplugin({
        name:'nick'
    })]
}