#### webpack学习笔记

1. ###### 基本概念

   入口：起点指示webpack应该使用那个模块，来作为构建其内部依赖图的开始，默认是./src/index.js，可以配置entry属性来指定入口。

   输出：告诉webpack在哪里输出所创建的bundle，以及如何命名这些文件，输出默认值是./dist/main.js，可以通过output来指定出口。

   loader：loader让webpack有能力去处理其他类型的文件，并将他们转化为有效模块，以供他们使用，以及被添加到依赖图中。

   plugin：loader用于转换某些类型的模块，而插件则可以用于执行范围更广的任务，包括：打包优化，资源管理，注入环境变量。使用插件可以通过require导入，再添加到plugins数组中。

2. ###### 入口起点

   ```JavaScript
   module.exports = {
     //注入单文件  
     entry: './path/to/my/entry/file.js', 
     //一次注入多个依赖文件
     entry: ['./src/file_1.js', './src/file_2.js'],
     output: {
       filename: 'bundle.js',
     },
   };
   
   ```

   

   ```JavaScript
   module.exports = {
     entry: {
       app: './src/app.js',
       adminApp: './src/adminApp.js',
     },
   }
   ```

   通过对象的语法，来配置具有更可扩展性的入口。

   入口对象的属性有：

   - dependOn：当前入口所依赖的入口，需要在入口被加载前加载

   - filename：指定输出的文件名称

   - import：启动时需=加载的模块

   - library：指定library选项，为当前的entry构建一个library

   - runtime：运行时chunk 的名字

   - publicPath：当该入口的输出文件在浏览器中被引用时，为他们指定一个公共url地址

     注意事项：

   - runtime和depenOn不应在同一个入口上同时使用
   - runtime不能指向已存在的入口名称
   - dependOn不能是循环引用

   

3. ###### 输出

   可以通过配置output选项，告诉webpack如何向硬盘写入编译文件。可以存在多个entry起点，但只能指定一个output配置。

4. ###### loader

   loader用于对模块的源代码进行转换。loader可以再加载文件时进行预处理，类似于其他构建工具中的任务，并提供了处理前端构建步骤的得力方式。

5. ###### plugin



垃圾  重写

1. 前置知识

   关于模块化的知识。

2. 

