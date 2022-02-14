const koa = require('koa')
const router = require('@koa/router')

const app = new koa()
const route = new router()

route.get('/', ctx => {
    ctx.body = 'hello koa /'
})

route.get('/about', ctx => {
    ctx.body = 'hello koa about'
})

app.use(route.routes())

app.listen(3001,() => {
    console.log('koa....')
})