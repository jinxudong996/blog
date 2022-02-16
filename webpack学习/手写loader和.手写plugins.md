#### loader

##### 特性

- loader只是一个导出为函数的JavaScript模块。

- 当有多个loader时，顺序从后往前（原理就是采用Compose）
- 多个loader串行执行，前一个的执行结果传递给后一个

##### 传参

可以通过loader-utils获取loader传递的参数

```javascript
{
	loader:path.join(__dirname,'./src/a.js'),//自定义的loader
	options:{
		name:'test'
	}
}
```

```javascript
const loaderutils = require('loader-utils')

module.exports = function(source){
	const {name} = loaderutils.getOptions(this)
	console.log(name)//即可获取传入的参数
}
```

##### 异步loader

通过this.async()将结果返回出去

```javascript
module.exports = function(source){
	const {name} = loaderutils.getOptions(this)
	
	const callback = this.async()
	
	fs.readFile(path.join(__dirname,'./a.txt'),(err,data)=>{
		if(err){
			callback(err)
		}
		callback(null,data)
	})
	
	console.log(name)//即可获取传入的参数
}
```

##### 手写loader

接下来手写一个自动合成雪碧图的loader

合成图片需要用到一个库[spritesmith](https://www.npmjs.com/package/spritesmith)，用法也比较简单，

```javascript
// Load in dependencies
var Spritesmith = require('spritesmith');
 
// Generate our spritesheet
var sprites = ['fork.png', 'github.png', 'twitter.png'];
Spritesmith.run({src: sprites}, function handleResult (err, result) {
  result.image; // Buffer representation of image
  result.coordinates; // Object mapping filename to {x, y, width, height} of image
  result.properties; // Object with metadata about spritesheet {width, height}
});
```

- 功能编写

  ```javascript
  // Load in dependencies
  var Spritesmith = require('spritesmith');
  const fs = require('fs');
  const path = require('path');
  // Generate our spritesheet
  var sprites = ['./image/a.jpg', './image/b.jpg'];
  
  Spritesmith.run({src: sprites}, function handleResult (err, result) {
  
    console.log(result.image); // Buffer representation of image
    console.log(result.coordinates); // Object mapping filename to {x, y, width, height} of image
    console.log(result.properties); // Object with metadata about spritesheet {width, height}
    fs.writeFileSync(path.join(__dirname,'dist/sprite.jpg'),result.image)
  });
  ```

  也是比较简单的一个功能，就是根据两张图片利用Spritesmith拼接到一起，然后使用writeFileSync写入到dist/sprite.jpg，打开dist目录即可看到合成的图片。

- loader编写

  首先loader使用是通过`background:url()`来输入要加载的图片，于是新建index.css

  ```css
  .img1{
      background:url(../image/a.jpg?__sprite)
  }
  .img2{
      background:url(../image/b.jpg?__sprite)
  }
  ```

  新建run-loader.js，通过loader-runner来验证编写的loader。loader-runner详细用法可看[文档](https://github.com/webpack/loader-runner)

  ```javascript
  const fs = require('fs');
  const path = require('path');
  const {runLoaders} = require('loader-runner');
  
  runLoaders(
      {
          resource:"./loaders/index.css",
          loaders:[path.resolve(__dirname,"./loaders/sprite-loader.js")],
          readResource:fs.readFile.bind(fs),
  
      },
      (err,result) => {err? console.log(err) : null}
  )
  ```

  现在正式开始编写sprite-loader

  ```javascript
  var Spritesmith = require('spritesmith');
  const fs = require('fs');
  const path = require('path');
  
  module.exports = function (source) {
      const callback = this.async();
      const imgs = source.match(/url\((\S*)\?__sprite/g);
      const matchedImgs = []
  
      console.log('imgs',imgs)
      for(let i=0;i<imgs.length;i++){
          const img = imgs[i].match(/url\((\S*)\?__sprite/)[1]
          matchedImgs.push(path.join(__dirname,img))
      }
      console.log('matchedImgs',matchedImgs)
      Spritesmith.run({
          src:matchedImgs,
      },(err,result) => {
          fs.writeFileSync(path.join(process.cwd(),'dist/sprite.jpg'),result.image)
          source = source.replace(/url\((\S*)\?__sprite/g,(match) => {
              return `url('dist/sprite.jpg')`
          })
          fs.writeFileSync(path.join(process.cwd(),'dist/index.css'),source)
          callback(null,source)
      })
  }
  ```

  Spritesmith的第一个参数需要合成图片的路径，首先要做的就是拼接待合成图片的路径数组，首先拿到loader参数，即`background:url()`，放到imgs数组中，接下来遍历数组，拿到url中的参数拼接成绝对路径，即matchedImgs数组。接下来就开始使用Spritesmith.run函数合成图片，并将合成图片写到`dist/sprite.jpg`文件里，同时替换loader参数为新的合成图片。

  [代码地址](https://github.com/jinxudong996/blog/tree/main/webpack%E5%AD%A6%E4%B9%A0/code/sprite-loader)

#### plugins

插件没有向loader那样独立的运行环境，只能在webpack中运行。

其基本结构为

```javascript
class MyPlugin{
	apply(compiler){
		compiler.hooks.done.tap('MyPlugin',() => {
			,,,
		})
	}
}
module.exports = MyPlugin
```

使用时就比较简单了，

```
plugins:[new MyPlugin]
```

接下来写一个简易的插件，首先新建`my-plugins.js`文件

```javascript
module.exports = class  Myplugin {
    constructor(options){
        this.options = options
    }
    apply(compiler){
        console.log('插件执行了')
        console.log(this.options)
    }
}
```

随后新建`webpack.config.js`

```javascript
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
```

运行打包命令，即可看见在命令行的输出。

[代码地址](https://github.com/jinxudong996/blog/tree/main/webpack%E5%AD%A6%E4%B9%A0/code/sprite-loader)

