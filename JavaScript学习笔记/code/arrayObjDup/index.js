let arrObj = [
  {id:15,name:'a15'},
  {id:16,name:'b16'},
  {id:17,name:'c'},
  {id:18,name:'d'},
  {id:16,name:'a15'},
  {id:15,name:'a16'},
]

// function unique(arr,prop){
//   let arrName = []
//   let newArray = []
//   arr.forEach(element => {
//     if(!arrName.includes(element[prop])){
//       arrName.push(element[prop])
//       newArray.push(element)
//     }
//   });
//   return newArray
// }

// function unique(arr,prop){
//   let result = []
//   let obj = {}
//   arr.forEach((element,index) => {
//     if(!obj[element[prop]]){
//       obj[element[prop]] = true
//       result.push(element)
//     }
//   });
//   return result
// }

// function unique(arr,prop){
//   var obj = {};
//   return arr.reduce((prev,cur)=>{
//     obj[cur[prop]] ? '':obj[cur[prop]] = true && prev.push(cur);
//     return prev
//   },[]);
// }
var obj = {};
var arr = [
  {id: 1,city: '南京'},
  {id: 2,city: '南京'}, 
  {id: 3,city: '杭州'}, 
  {id: 4,city: '广州'},
  {id: 5,city: '广州'},
  {id: 5,city: '6'}
];
function unique(arr,prop){
  for (var i = 0; i < arr.length - 1; i++) {
    for (var j = i + 1; j < arr.length; j++) {
      if (arr[i][prop] == arr[j][prop]) {
        arr.splice(j, 1); 
        j--; // 因为数组长度减小1，所以直接 j++ 会漏掉一个元素，所以要 j--
      }
    }
  }
  return arr
}

// console.log(arr)
console.log(unique(arrObj,'id'))

// console.log(unique(obj,'id'))