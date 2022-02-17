let map = new Map();
let weakmap = new WeakMap();

// ((function(){
//     let a = 1
// })())
(function () {
    const foo = { name: 'foo' }
    const bar = { name: 'bar' }

    map.set(foo, 1)
    weakmap.set(bar, 1)
    console.log(weakmap)
}());

for (let item of map.entries()) {
    console.log(item[0], item[1]);
}

console.log(weakmap)
