const fs = require('fs')
const path = require('path')
const {marked} = require('marked')
const browserSync = require('browser-sync')

let mdPath = path.join(__dirname, process.argv[2])
let cssPath = path.resolve('index.css')
let htmlPath = mdPath.replace(path.extname(mdPath), '.html')

fs.readFile(mdPath, 'utf-8', (err, data) => {
  // 将 md--》html
  let htmlStr = marked(data)
  console.log(htmlStr)
  fs.readFile(cssPath, 'utf-8', (err, data) => {
    let retHtml = temp.replace('{{content}}', htmlStr).replace('{{style}}', data)
    // 将上述的内容写入到指定的 html 文件中，用于在浏览器里进行展示
    fs.writeFile(htmlPath, retHtml, (err) => {
      console.log('html 生成成功了')
    })
  })
})

browserSync.init({
  browser: '',
  server: __dirname,
  watch: true,
  index: path.basename(htmlPath)
})

const temp = `
      <!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <title></title>
          <style>
              .markdown-body {
                  box-sizing: border-box;
                  min-width: 200px;
                  max-width: 1000px;
                  margin: 0 auto;
                  padding: 45px;
              }
              @media (max-width: 750px) {
                  .markdown-body {
                      padding: 15px;
                  }
              }
              {{style}}
          </style>
      </head>
      <body>
          <div class="markdown-body colorRed">
              {{content}}
          </div>
      </body>
      </html>
  `