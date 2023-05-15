const fs = require('fs')
const express = require('express')

const server = express()

server.use('/dist',express.static('./dist'))

const serverBundle = require('./dist/vue-ssr-server-bundle.json')
const template = fs.readFileSync('./index.template.html','utf-8')
const clientManifest = require('./dist/vue-ssr-client-manifest.json')
// const clientManifest = require('./dist/vue-ssr-client-manifest.json')
 
const renderer = require('vue-server-renderer').createBundleRenderer(serverBundle,{
  template,
  clientManifest
})

server.get('/',(req,res) => {

  // const app = new Vue({
  //   template:`
  //     <div id="app">
  //       <h1>{{message}}</h1>
  //       <input type="text" v-model="num">
  //       <button @click="onclick"></button>
  //     </div>
  //   `,
  //   data(){
  //     return{
  //       message:'这是啥',
  //       num:12
  //     }
  //   },
  //   methods:{
  //     onclick(){
  //       console.log('点击事件')
  //       this.num ++
  //     }
  //   }
  // })

  renderer.renderToString({
    title:'ssr',
    meta:`<meta name="description" content="这里是ssr的meta标签">`
  }, (err,html) => {
    if(err) {
      return res.status(500).end('服务端错误')
    }
    res.setHeader('Content-Type', 'text/html; charset=utf8')
    console.log('#########################################')
    console.log(html)
    console.log('#########################################')
    res.end(html)
  })
})

server.listen(3131,() => {
  console.log('服务端跑起来了:',3131)
})
