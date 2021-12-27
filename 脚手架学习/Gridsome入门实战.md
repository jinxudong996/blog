Gridsome 是一个免费的、开源的、基于vue.js技术栈的静态网站生成器，[文档地址](https://www.gridsome.cn/docs/)。

静态网站生成器是使用一系列配置、模板以及数据生成HTML文件及相关资源的工具。这个功能也叫预渲染，生成的网站不需要JAVA这样的服务器，只需要放到支持Web Server或CDN上即可运行。

这类网站生成器也被称为JAMStack，JAMStack的JAM就是JavaScript、API和Markup的首字母组合。本质上就是一种胖前端，通过调用各种API来实现更多的功能。

#### 入门

##### 项目安装

```
npm install --global @gridsome/cli
gridsome create my-gridsome-site
cnpm install
```

随后在命令行运行`gridsome develop`启动项目，在浏览器输入`http://localhost:8080/`即可查看项目界面。

##### 目录结构

```
src
├── components     # 公共组件 
├── layouts		   # 布局组件
├── pages          # 路由页面  自动生成路由
├── templates	   # 放置集合的节点
├── main.js        # 项目入口 
├── favicon.png    # 项目入口的图片
static             # 放置静态资源  不需要打包的
gridsome.config.js   #gridsome配置相关 安装插件
gridsome.server.js   #gridsome配置文件 用于连接到 Gridsome 服务器的各个部分。该文件必须导出一个可以访问 API 的函数

```

详细配置可查看官方[文档](https://www.gridsome.cn/docs/directory-structure/)

##### 项目配置

 Gridsome 需要 gridsome.config.js 才能工作。插件和项目设置位于此处 

- seteName

  设置项目名称

- siteDescription

  设置<meta>标签为首页添加描述

- pathPrefix

  Gridsome 假设您的项目是从域的根目录提供的。如果您的项目将托管在名为 my-ap 的子目录中，请将此选项更改为“/my-app” 

- titleTemplate

  标题模板， 使用%s 占位符被替换为您在页面中设置的 metaInfo 的标题 ， 默认就是%s - <siteName> 

- templates

   为集合定义路由和模板 

- plugins

   通过将插件添加到插件数组来激活插件 

##### pages

页面负责在 URL 上显示您的数据。每个页面都将静态生成并拥有自己的带有标记的 index.html 文件。

有两周方式来创建pages

- 直接在pages目录下创建文件， src/pages 目录中的单个文件组件将自动可用它们自己的 URL 

- 在`gridsome.server.js`使用 `createPages`  来创建

  ```
  module.exports = function (api) {
    api.createPages(({ createPage }) => {
      createPage({
        path: '/my-page',
        component: './src/templates/MyPage.vue'
      })
    })
  }
  ```

  



##### 添加集合

集合是一组节点，每个节点都包含带有自定义数据的字段，同事将节点与渲染成页面。

- 使用插件添加集合

```javascript
// gridsome.config.js
module.exports = {
  plugins: [
    {
      use: '@gridsome/source-wordpress',
      options: {
        baseUrl: 'YOUR_WEBSITE_URL',
        typeName: 'WordPress',
      }
    }
  ]
}
```



- 使用api添加集合

```javascript
// gridsome.server.js
const axios = require('axios')

module.exports = function (api) {
  api.loadSource(async actions => {
    const collection = actions.addCollection('Post')

    const { data } = await axios.get('https://api.example.com/posts')

    for (const item of data) {
      collection.addNode({
        id: item.id,
        title: item.title,
        content: item.content
      })
    }
  })
```

#####  GraphQL 查询数据

添加的集合都被放在 GraphQL 数据层，可以使用`<page-query>`或者`<static-query>`标签 将 GraphQL 数据层中的数据查询到任何页面、模板或组件中。

- 使用`<page-query>`

```javascript
<template>
  <div>
    <div v-for="edge in $page.posts.edges" :key="edge.node.id">
      <h2>{{ edge.node.title }}</h2>
    </div>
  </div>
</template>

<page-query>
query {
  posts: allWordPressPost {
    edges {
      node {
        id
        title
      }
    }
  }
}
</page-query>
```

查询的数据也可以进行各种排序分页等操作：

| Argument    | Default  | Description                                                  |
| :---------- | :------- | :----------------------------------------------------------- |
| **sortBy**  | `"date"` | Sort by a node field.                                        |
| **order**   | `DESC`   | Sort order (`DESC` or `ASC`).                                |
| **sort**    |          | Sort by multiple node fields.                                |
| **skip**    | `0`      | How many nodes to skip.                                      |
| **limit**   |          | How many nodes to get.                                       |
| **page**    |          | Which page to get.                                           |
| **perPage** |          | How many nodes to show per page. Omitted if no `page` argument is provided. |
| **filter**  | `{}`     | [Read more](https://www.gridsome.cn/docs/filtering-data/).   |

- 使用`<static-query>`

```html
<template>
  <div v-html="$static.post.content" />
</template>

<static-query>
query {
  post(id: "1") {
    content
  }
}
</static-query>
```



##### 模板渲染节点

模板用于为集合中的节点创建单个页面。节点需要相应的页面才能显示在其自己的 URL 上 。

在`gridsome.config.js`中进行设置：

```
module.exports = {
  templates: {
    Post: [
      {
        path: '/blog/:year/:month/:title',
        component: './src/other/location/Post.vue'
      }
    ]
  }
}
```

通过id查询指定模板的数据：

```html
<template>
  <div>
    <h1 v-html="$page.post.title" />
    <div v-html="$page.post.content" />
  </div>
</template>

<page-query>
query ($id: ID!) {
  post(id: $id) {
    title
    content
  }
}
</page-query>
```

#### 进阶

接下来做一个blog项目，使用[startbootstrap-clean-blog](https://github.com/StartBootstrap/startbootstrap-clean-blog)的ui，根据这个ui先对项目进行初始化。

