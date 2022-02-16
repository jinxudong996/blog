// Load in dependencies
var Spritesmith = require('spritesmith');
const fs = require('fs');
const path = require('path');
// Generate our spritesheet
var sprites = ['./image/a.jpg', './image/b.jpg'];

Spritesmith.run({src: sprites}, function handleResult (err, result) {

  console.log(result.image); // Buffer representation of image
  console.log(result.coordinates); // Object mapping filename to {x, y, width, height} of image
  console.log(result.properties); // Object with metadata about spritesheet {width, height}
  fs.writeFileSync(path.join(__dirname,'dist/sprite.jpg'),result.image)
});