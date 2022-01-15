
function selectSort(arr){
	let minIndex = 0;
	let len = arr.length
	for(let i=0; i< len;i++){
		minIndex = i
		for(let j=i+1;j<len;j++){
			if(arr[j] < arr[minIndex]){
				minIndex = j
			} 
		}
		[arr[i],arr[minIndex]] = [arr[minIndex],arr[i]]
	}
	return arr
}

let arr = [6,5,4,3,2,1]
console.log(selectSort(arr))