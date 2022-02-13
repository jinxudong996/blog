const express = require('express')

const router = express.Router()

router.get('/foo',(req,res) => {
    res.send('foo')
})

module.exports =  router