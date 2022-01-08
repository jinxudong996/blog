class ArrayQueue{
    constructor(n){
        this.items = []
        this.n = n //栈的大小
        this.head = 0 //队列头部下标
        this.tail = 0 //队列尾部下标
    }
    //入栈
    push(item){
        if(tail) == n) return
        this.items[this.tail] = item
        ++tail
        return
    }
    //出栈
    pop(){
        if(this.head  == this.tail) return
        let tmp = this.items[this.head]
        ++this.head
        return tmp
    }
}