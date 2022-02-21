const o1 = {
    text:'o1',
    fn:function(){
        console.log(this.text)
    }

}

const o2 = {
    text:'o2',
    fn:function(){
        o1.fn.apply(o2)
        // console.log(this.text)
       
    }

}

const o3 = {
    text:'o3',
    fn:function(){
        var f = o1.fn
        f ()
    }

}

// o1.fn()
//  o2.fn()
o2.fn.apply(o1)

//  console.log(this)