###### DOM文档对象模型

文档对象模型时HTML和XML文档的编程接口。DOM表示由多层节点构成的文档，通过它开发者可以添加、修改和删除页面的各个部分。

###### 节点层级

任何HTML文档都可以用DOM表示为一个由节点构成的层级结构。

其中document节点表示每个文档的根节点，有一个唯一的子节点<html>文档元素，文档元素是文档最外围的元素，其他所有的元素都在这个元素之内。HTML中的每段标记都可以表示为这个树形结构中的一个节点，元素节点为HTML元素，属性节表示属性，文档类型节点表示文档类型，注释节点表示注释。DOM中总共有12种节点类型，常用的就是文本节点和元素节点。

###### document类型

document类型时JavaScript中表示文档节点的类型。在浏览器中，文档对象document是HTMLDocument的实例，表示整个HTML页面，document是window对象是属性。document类型的节点，其nodeType是9，nodeName值为“#document”，nodeValue值为null。document对象可以用于获取关于页面的信息以及操纵其外观和底层结构。

- document.documentElement属性始终指向HTML页面的<html>元素

- document.body属性指向页面的<body>元素。
- document.title  包含<title>元素中的文本
- doucment.URL  包含当前页面的完整URL
- doucment.domain 页面的域名
- doucment。referrer  包含链接到当前页面的URL

###### Element类型

Element类型表示XML或者HTML元素，对外暴露出访问元素签名、子节点和属性的能力。

每个元素都有零个或多个属性，通常用于为元素或内容附加更多信息。常用的方法主要有三个：

getAttribute（）、setAttribute（）和removeAttribute（）。

###### Text类型

知识点：

- nodeName与nodeValue保存着有关节点的信息。这两个
- 每个节点都有一个childNodes属性，其中包含一个nodeList实例，nodeList是一个类数组对象，用于存储可以按位置存取的有序节点。它其实是一个对DOM结构的查询，DOM结构的变化会自动地在NodeList中反映出来，通常被说成实时的活动对象。
- 每个节点都有parentNode属性，指向其DOM树中的父元素。
- appendChild()用于在列表末尾添加到节点，添加节点会更新相关的关系指针。insertBefore（）方法可以指定位置插入节点。replaceChild（）方法可以替换指定节点。