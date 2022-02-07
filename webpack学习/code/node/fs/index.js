const fs = require('fs')
const path = require('path')

// fs.readFile(path.resolve('data.txt'), 'utf-8', (err, data) => {
//     console.log(err)
//     console.log(data)
// })

// fs.writeFile('data.txt', 'hello nodeJs', (err) => {
//     if (!err) {
//         fs.readFile(path.resolve('data.txt'), 'utf-8', (err, data) => {
//             console.log(data)
//         })
//     }
// })

// fs.appendFile('data.txt',' 追加成功',(err) => {
//     console.log('追加成功~~')
// })

// fs.copyFile('data.txt','text.txt',(err) => {
//     console.log("copy success~~")
// })

// fs.watchFile('data.txt',{interval:20},(curr,prev) => {
//     if(curr.mtime !== prev.mtime){
//         console.log('文件被修改了')
//         fs.unwatchFile('data.txt')
//     }
// })

fs.open(path.resolve('data.txt'), 'r', (err, fd) => {
    console.log(err)
    console.log(fd)
})