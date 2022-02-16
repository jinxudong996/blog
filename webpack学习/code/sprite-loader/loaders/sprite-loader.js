var Spritesmith = require('spritesmith');
const fs = require('fs');
const path = require('path');

module.exports = function (source) {
    const callback = this.async();
    const imgs = source.match(/url\((\S*)\?__sprite/g);
    const matchedImgs = []

    console.log('imgs',imgs)
    for(let i=0;i<imgs.length;i++){
        const img = imgs[i].match(/url\((\S*)\?__sprite/)[1]
        matchedImgs.push(path.join(__dirname,img))
    }
    console.log('matchedImgs',matchedImgs)
    Spritesmith.run({
        src:matchedImgs,
    },(err,result) => {
        fs.writeFileSync(path.join(process.cwd(),'dist/sprite.jpg'),result.image)
        source = source.replace(/url\((\S*)\?__sprite/g,(match) => {
            return `url('dist/sprite.jpg')`
        })
        fs.writeFileSync(path.join(process.cwd(),'dist/index.css'),source)
        callback(null,source)
    })
}