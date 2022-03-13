lerna学习笔记

lerna是一个优化基于git+npm的多package项目的管理工具，可以大幅减少重复操作，提升操作的标准化。

> lerna是一个架构优化的产物，它揭示了一个架构真理：项目复杂度提升后，就需要对项目进行架构优化。架构优化的主要目标往往都是以效能为核心。

##### 常用命令

- lerna create package  创建package
- lerna add  安装依赖
- lerna link  链接依赖
- lerna exec 执行shell脚本
- lerna run 执行npm命令
- lerna clean 清空依赖
- lerna bootstrap 重装依赖
- lerna changed 查看版本变更
- lerna publish 项目发布

#####  实例

接下来使用这些api做一些小案例，加深下印象。

首先`npm init`初始化我们的项目，`npm install lerna -g`全局安装lerna，创建两个包，core和utils，

- 安装依赖

  如果想安装webpack，可以使用`lerna add webpack`，可以看到我们的core模块和utils模块全部都安装了webpack，如果想指定某一个模块安装依赖，需要指定`lerna add webpack-cli packages/core  `这里就只为core模块安装了依赖。

- lerna clean会清空依赖，但是package.json里的dependencies中的依赖列表并不会删除，需要手动删除。重新安装依赖：lerna bootstrap

- lerna link 如果模块有互相依赖的话，可以使用改命令添加软连接。