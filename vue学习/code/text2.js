const {arrExtend} = require('./copyArr')

let arr = [0,1,2,3,4] 

if (Array.isArray(arr)) {
    arr.__proto__ = arrExtend
    arr[5] = 5
 }

 console.log(arr)