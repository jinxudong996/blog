MongoDB学习笔记

##### 简介

在数据量暴增的时代，用传统的关系型数据库来满足数据高并发读写、巨量数据存储、数据库的扩展和高可用，就需要增加软硬件的规格，将大幅度提高成本。NoSQL应运而生，意思就是不仅仅是SQL，即非关系系型数据库。

NoSQL主要有一下几种：

- 键值数据库，使用数据结构中的键key来查找特定的数据value，这类数据有着极高的读写性能，用于处理大量数据的高访问负载较为合适。主要有Redi、Flare
- 文档型数据库，满足海量数据的存储和访问需求，同时对字段要求不严格，可以随意增、删除。主要有MongoDB，CouchDB
- 列存储型数据路，查找速度快，可扩展性强，适合做分布式文件存储系统，主要有：Cassandra、Hbase
- 图数据库，利用图结构的相关算法来存储实体之间的关系信息，适合用于构建社交网络和推荐系统的关系图谱，主要有infoGrid、Neo4J

- 而MongoDB 是一个基于分布式文件存储的数据库。由 C++ 语言编写。旨在为 WEB 应用提供可扩展的高性能数据存储解决方案。

- MongoDB 是一个介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最像关系数据库的。

其适用场景主要有以下几点：

- 需要大量低价值数据，且对数据处理性能有较高要求
- 需要借助缓存层来处理数据
- 需要高纬度的伸缩性

##### 基本概念

- 数据存储结构：MongoDB是文档型库，其中存储的数据就是熟悉的JSON格式。可以把MongoDB数据库想象为一个超级大对象，对象里有不同的集合，集合中有不同的文档。其中集合Collections对应关系型数据库中的表Table，文档Document对应行Row，数据字段Field对应列Column

- 数据库

  展示数据库`show dbs`

  新建或者使用数据库  `use dbsname`

  展示当前数据库  `db`

  删除数据库 `db.dropDatabase()`

- 集合

  显示集合`show collections`

  新建集合`db.hello.insert({a:1,b:2})`

  显示创建集合：`db.createCollection()`

- 文档

  文档对字段名称有以下限制：

  - 字段名称`_id`保留用作主键，它的值在集合中必须是唯一的，不可变的，并且是数组以外的任何类型
  - 字段名称不能包含空字符

##### 

##### 基本操作

- 查找

  - find  查找所有，`dn.name.find()`，等价于`select * from table`
  - find({},{item:1})  查询指定字段
  - find({status：‘D’})相等条件查询，等价于`select * from table where status='D'`
  - find({$or:[{status:A},{qty:100}]})  等价于 `select * from table where status=A or qty=100`

- 新增

  db.collection.insertOne()  插入单个文档到集合中

  db.collection.insertMany()  插入多个文档到集合中

  db.collection.insert()  插入一个或多个文档到集合中

- 更新

  db.collection.updateOne()  更新单个文档

  db.collection.updateMany()  更新多个文档

  db.collection.replaceOne()  替换指定文档

- 删除

  db.collection.deleteMany()  删除多个文档

  db.collection.deleteOne()  删除单个文档

##### nodeJs中连接MongoDB

需要安装mongodb包，

```javascript
const { MongoClient } = require('mongodb')

const client = new MongoClient('mongodb://127.0.0.1:27017')

async function run() {
  try{
    await client.connect()
    const db = client.db('abc')
    const collectionName = db.collection('name')
    const ret = await collectionName.find()
    console.log(await ret.toArray())
  } catch(err) {
    console.log('连接失败',err)
  }
}

run()
```







