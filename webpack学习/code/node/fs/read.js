const fs = require('fs')

let buf = Buffer.alloc(10)

fs.open('data.txt','r',(err,fd) => {
    console.log(fd)
    fs.read(fd,buf,0,4,0,(err,readBytes,data) => {
        console.log(readBytes)
        console.log(data)
        console.log(data.toString())
    })
})