let arr1 = [1,2,3]
let arr2 = [4,5,7]

function add(a1,a2){
  let newArr = []
  let n = 0;
  let curent = 0;

  for(let i=arr1.length-1;i>=0;i--){
    if(a1[i] + a2[i] + n >= 10){
      newArr.unshift(0)
      n = 1;
    }else{
      if(n == 1){
        newArr.unshift(a1[i] + a2[i] + 1)
        n = 0
      }else{
        newArr.unshift(a1[i] + a2[i])
      }
      
    }
  }

  return newArr;
}

// add(arr1)
console.log(add(arr1,arr2))