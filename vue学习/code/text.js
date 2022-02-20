let obj = {name:'nick',age:18}

let p = new Proxy(obj,{
    ownKeys(target){
        console.log("捕获到了")
        return Reflect.ownKeys(target)
    }
})
for (let key in p){
    console.log(key,'...',obj[key])
}
// console.log('name' in p)