function insertionSort(arr) {
    let len = arr.length
	
	for(let i=0;i<len;i++){
		for(let j=0; j<i;j++){
			if(arr[i] < arr[j]){
				[arr[i],arr[j]] = [arr[j],arr[i]]
			}
		}
	}
	return arr
}

let arr = [6,5,4,3,2,1]
console.log(insertionSort(arr))
