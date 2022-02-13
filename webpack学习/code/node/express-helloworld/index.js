const express = require('express')
const MRrouter = require('./mr.js')

const app = express()

app.use(MRrouter)
app.use('/about',(req,res,next) => {
    console.log(req.method,req.url,Date.now())
    next()
})
app.use('/about',(req,res,next) => {
    console.log(req.method,req.url,Date.now())
    next()
})

// app.use((req,res,next) => {
//     console.log(req.method,req.url,Date.now())
//     next()
// })

app.get('/',(req,res) => {
    res.send('hello,world')
})

app.get('/about',(req,res) => {
    res.send('hello,about')
})

app.use((err,req,res,next) => {
    console.log('错误')
    res.status(500).json({
        error:err.message
    })
})

app.listen(3000,() => {
    console.log('server start---')
})