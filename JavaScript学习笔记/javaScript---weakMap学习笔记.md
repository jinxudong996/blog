#### 数组去重

###### indexOf

```javascript
var array = [1, 1, '1'];

function unique(array) {
    var res = [];
    for (var i = 0, len = array.length; i < len; i++) {
        var current = array[i];
        if (res.indexOf(current) === -1) {
            res.push(current)
        }
    }
    return res;
}

console.log(unique(array)); //[ 1, '1' ]
```

这种方式比较常规，就是新建一个数组，遍历待去重数组，在新数组中调用`indexOf`检测如果没有改项就添加到新数组中。

###### 排序后去重

```javascript
var array = [1,100,8,9,8000,1,9]

function unique(array) {
    var res = [];
    var sortedArray = array.sort((a,b) => { return b - a });
    var seen;
    for (var i = 0, len = sortedArray.length; i < len; i++) {
        // 如果是第一个元素或者相邻的元素不相同
        if (!i || seen !== sortedArray[i]) {
            res.push(sortedArray[i])
        }
        seen = sortedArray[i];
    }
    return res;
}

console.log(unique(array)); 
//[ 8000, 100, 9, 8, 1 ]
```

首选排序下，进行遍历，将遍历的值用个变量存储下，下次遍历时进行对比，如果不一致就塞进申明的新数组里。

###### filter

```javascript
var array = [1, 2, 1, 1, '1'];

function unique(array) {
    var res = array.filter(function(item, index, array){
        return array.indexOf(item) === index;
    })
    return res;
}

console.log(unique(array));
```

这种方式主要是利用`indexOf`方法来判断返回的数值和当前的序列号是否一致，配合过滤函数来完成去重，还是蛮巧妙的。

###### set

ES6新增了set()，去重就很简单了。

```javascript
var unique = (a) => [...new Set(a)]
```



#### 求最大值

```
Math.max(value1[,value2, ...]) 
```

> 返回给定的一组数字中的最大值。如果给定的参数中至少有一个参数无法被转换成数字，则会返回 [`NaN`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/NaN)。 

```javascript
var arr = [6, 4, 1, 8, 2, 11, 23];
console.log(Math.max(...arr))
```

上面是使用静态方法`Math.max`来获取最大值，也可以排序来获取：

```javascript
var arr = [6, 4, 1, 8, 2, 11, 23];

arr.sort(function(a,b){return a - b;});
console.log(arr[arr.length - 1])
```



#### 数组扁平化

就是将多维数组展开转化为一个一维数组，

```javascript
var arr = [1, [2, [3, 4]]];

function flatten(arr) {
    var result = [];
    for (var i = 0, len = arr.length; i < len; i++) {
        if (Array.isArray(arr[i])) {
            result = result.concat(flatten(arr[i]))
        }
        else {
            result.push(arr[i])
        }
    }
    return result;
}
```

通过`Array.isArray`来判断数组某一项如果是数组就递归调用该函数，如果不是就存放到新数组里。

如果数组的元素是纯数字，可以用toString方法：

```javascript
function flatten(arr) {
    return arr.toString().split(',').map(function(item){
        return Number(item)
    })
}
```



