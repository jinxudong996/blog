let arr = [0,1,2,3]
obj = {
    age:[1,2,3],
    name:'nick'
}

Object.defineProperty(obj,'age',{
    get(val){
        console.log('1111',val)
        return val
    }
})


console.log(obj.age)