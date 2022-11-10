let name = 'gg'

let a = {
  name:'aa',
  f1:function () {
    console.log(this.name)
  }
}

let b = {
  name:'bb',
  f2 : function () {
    console.log(this.name)
  }
}


let f = b.f2();
