const fs = require('fs')

let buf = Buffer.from('0123456789')

fs.open('b.txt','w',(err,fd) => {
    fs.write(fd,buf,0,5,0,(err,writen,buffer) =>{
        console.log(writen)
        console.log(buffer)
        console.log(buffer.toString())
    })
})