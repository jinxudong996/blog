const Vue = require('vue');
const server = require('express')();

const template = require('fs').readFileSync('./index.template.html', 'utf-8');

const renderer = require('vue-server-renderer').createRenderer({
  template,
});

const context = {
    title: 'vue ssr',
    meta: `
        <meta name="keyword" content="vue,ssr">
        <meta name="description" content="vue srr demo">
        <meta charset="utf-8">
    `,
};

server.get('*', (req, res) => {
  const app = new Vue({
    data: {
      url: req.url
    },
    template: `<div @click="onClick">现在访问的 URL 是： {{ url }}</div>`,
    mrthods:{
      onClick(){
        console.log('dianji..')
      }
    }
  });

  renderer
  .renderToString(app, context, (err, html) => {
    console.log(html);
    if (err) {
      console.log(err)
      res.status(500).end('Internal Server Error')
      return;
    }
    res.end(html);
  });
})

server.listen(8080,() => {
  console.log('监听。。。8080')
})