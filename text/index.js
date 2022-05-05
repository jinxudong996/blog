function n(){
  name:'nick'
}


n.prototype.color = 'red'

let n1 = new n()
n.prototype = {
  age:18
}
console.log(n1)
console.log(n1.age)
console.log(n1.color)