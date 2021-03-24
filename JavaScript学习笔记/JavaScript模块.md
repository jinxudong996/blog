JavaScript模块

在一个复杂度应用中，将代码按照一定的规则拆分到几个互相独立的文件中，通过对外暴露调用接口，与外部完成整合，每个文件彼此独立，模块之间又能够互相调用和通信，这就是模块化。

在ES6之前，常用的解决方案是通过立即执行函数，构造一个私有作用域，在通过闭包对外暴露接口。比如著名的JQuery就是这样做的：

```javascript
（function(window,$){
	var data = 'data'
	function foo(){
		console.log('this is foo')
	}
	
}）（window,jQuery）
```



ES6模块功能主要由export和import构成，export用于规定模块的对外接口，import用于带入模块提供的功能。

```
export const name = "nick"
import name from "./example.js"

if(name === 'nick'){
	import name from "./example.js"  //语法错误
}
```

export和import命令如果出现在块级作用域中，就会报一个语法错误，因为import语句的执行是在编译阶段，if语句毫无意义，这违背了ES6模块设计的初衷。将ES6设计成静态的，有一个非常明显的优势，通过静态分析能够分析出导入的依赖。如果导入的模块没有被使用，可以通过tree shaking等手段减少代码体积，进而提升运行性能。这就是基于ESM实现tree shaking的基础。