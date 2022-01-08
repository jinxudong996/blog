class stack{
    constructor(n){
        this.items = []
        this.n = n //栈的大小
        this.count = 0 //栈元素个数
    }
    //入栈
    push(item){
        if(count == n) return
        this.items[count] = item
        ++count
        return
    }
    //出栈
    pop(){
        if(count == 0) return
        let tmp = this.items[count-1]
        --this.count
        return tmp
    }
}