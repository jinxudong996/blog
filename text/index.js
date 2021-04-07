let ab = require('lodash ')

let b = {}
let a = {a1:b, a2:b}

console.log(a.a1 === a.a2) //true

let c = ab.cloneDeep(a)

console.log(c.a1 === c.a2) //false