前几天维护一个功能，真心感叹维护功能要比写难太多。遇到了一个数组对象去重的问题，憋了半天自己写了个，以前归纳过[数组去重](https://juejin.cn/post/7039880197574754335)，就归纳一下数组对象去重：

##### 将属性放到新数组里去重

这个方法就是自己写的，原理也比较简单，就是新建一个数组，将对象所有的属性放进去进行去重，再新建一个对象，根据去重时将对应的对象放进新数组即可：

```javascript
function unique(arr,prop){
  let arrName = []
  let newArray = []
  arr.forEach(element => {
    if(!arrName.includes(element[prop])){
      arrName.push(element[prop])
      newArray.push(element)
    }
  });
  return newArray
}
```

##### 根据对象属性去重

对象属性具有唯一性，可以据此新建一个对象，为新对象绑定属性，跟上面原理差不多，直接上代码：

```javascript
function unique(arr,prop){
  let result = []
  let obj = {}
  arr.forEach((element,index) => {
    if(!obj[element[prop]]){
      obj[element[prop]] = true
      result.push(element)
    }
  });
  return result
}
```

##### 根据数组reduce方法去重

```javascript
function unique(arr,prop){
  var obj = {};
  return arr.reduce((prev,cur)=>{
    obj[cur[prop]] ? '':obj[cur[prop]] = true && prev.push(cur);
    return prev
  },[]);
}
```

reduce方法mdn上看的比较迷惑，[掘金](https://juejin.cn/post/6844904025310117901)上这篇文章讲的很清晰。

> `Array.reduce()`接受两个参数：一个是对数组每个元素执行的回调方法，一个是初始值。
>
> 这个回调接收4个参数，前两个参数是：`accumulator`是当前聚合值，`current`是数组循环时的当前元素。无论你返回什么值，都将作为累加器提供给循环中的下一个元素。初始值将作为第一次循环的累加器。

##### 冒泡排序

```javascript
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
```

