let a = {
  name:'金旭东'
}

let b = Object.create(a)

b.name = '旺旺'

console.log(b.name)
console.log(a.name)
console.log(b.prototype)
console.log(a.constructor === b.prototype)