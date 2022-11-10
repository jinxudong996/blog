const p1 = {
  name:'jxd'
}

const p2 = Object.create(p1)
p2.name = 'aaa'
console.log(p1.name)
console.log(p2.name)