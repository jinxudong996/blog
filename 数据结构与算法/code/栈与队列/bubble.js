function bubbleSort(arr){
    let len = arr.length
    let sortFlag = false 
    for(let i=0; i<len;i++ ){
        for(let j=0; j<len-i-1; j++){
            if(arr[j] > arr[j+1]){
                let tmp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = tmp
                sortFlag = true
            }
        }
        if(!sortFlag) return
    }
    
}

let arr = [6,5,4,3,2,1]
bubbleSort(arr)
console.log(arr)