// 让 arrExtend 先继承 Array 本身的所有属性
const arrExtend = Object.create(Array.prototype)
const arrMethods = [
  'push',
  'pop',
  'shift',
  'unshift',
  'splice',
  'sort',
  'reverse'
]
/**
 * arrExtend 作为一个拦截对象, 对其中的方法进行重写
 */
arrMethods.forEach(method => {
  const oldMethod = Array.prototype[method]
  const newMethod = function(...args) {
    oldMethod.apply(this, args)
    console.log(`${method}方法被执行了`)
  }
  arrExtend[method] = newMethod
})
exports.arrExtend = arrExtend



// module.exports = {
//     arrExtend
// }