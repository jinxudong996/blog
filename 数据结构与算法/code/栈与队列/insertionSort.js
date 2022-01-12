function insertionSort(arr) {
    let len = arr.length
    for (let i = 1; i < len; i++) {
        let val = arr[i]
        let j = 0
        for (; j >= 0; j--) {
            if (arr[j] > val) {
                arr[j + 1] = arr[j];  // 数据移动
            } else {
                break;
            }
        }
        arr[j+1] = val; // 插入数据
    }
}

let arr = [6,5,4,3,2,1]
insertionSort(arr)
console.log(arr)