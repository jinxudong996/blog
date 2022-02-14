const express = require('./express')

const app = express()

app.get('/',(req,res) => {
    res.end('get /')
})

app.get('/foo',(req,res) => {
    res.end('get /foo')
})

app.listen(3001, () => {
    console.log('listen at 3001')
})