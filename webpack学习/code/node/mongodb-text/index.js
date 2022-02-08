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