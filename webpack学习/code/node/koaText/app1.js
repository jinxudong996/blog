const koa = require('koa')

const app = new koa()

const one = (ctx,next) => {
    console.log('1')
    next()
    console.log('one')
}

const two = (ctx,next) => {
    console.log('2')
    next()
    console.log('two')
}

const three = (ctx,next) => {
    console.log('3')
    next()
    console.log('three')
}

app.use(one)
app.use(two)
app.use(three)

app.listen(3001,() => {
    console.log('koa....')
})