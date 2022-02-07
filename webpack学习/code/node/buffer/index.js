// const b1 = Buffer.alloc(10)
// const b2 = Buffer.allocUnsafe(10)
// const b3 = Buffer.from('1')
// console.log(b3)

// let buf = Buffer.alloc(6)

// buf.fill('123')
// buf.write('123',1,2)
// buf.write('123456789')
// let b1 = buf.slice()
// console.log(buf.indexOf('4'))
// console.log(buf.toString())

let b1 = Buffer.from('123')
let b2 = Buffer.from('456')

b2.copy(b1)

console.log(b1.toString())
console.log(b2.toString())

