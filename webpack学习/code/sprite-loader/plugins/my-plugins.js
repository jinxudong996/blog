module.exports = class  Myplugin {
    constructor(options){
        this.options = options
    }
    apply(compiler){
        console.log('插件执行了')
        console.log(this.options)
    }
}