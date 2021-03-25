## JavaScript继承

###### 原型链继承

> 原型链是JavaScript主要的继承方式，基本思想就是通过原型继承多个引用类型的属性和方法。主要思路就是：每一个构造函数都有一个原型对象，原型对象上constructor属性指回构造函数，而新实例内部有一个内部指针指向原型对象。如果原型对象是另一个类型的实例，就意味着这个原型本身有一个有一个内部指针指向另一个原型，相应的另一个原型也有一个指针指向另一个构造函数，这样在原型与原型之间构造了一条原型链。

```JavaScript
function sub(){
    this.name = 'nick'
}
sub.prototype.getName = function() {
    return this.name
}

function sup() {
    this.age = 18
}

sup.prototype = new sub()

let sp = new sup()
console.log(sp.age)  //18
console.log(sp.name)  //nick
console.log(sp.getName())  //nick
```

sub的一个实例赋值给了sup的原型对象，实现了对sub的继承。

通过对象访问属性时，会按照这个属性的名称开始搜索，首先从对象本身开始，如果在对象的属性上发现了给定的名称，则返回名称对应的值；如果没找到，就会沿着指针进入原型对象，在原型对象上查找属性，如果在原型对象上发下了给定的名称，就返回名称指定的值；如果没找到，就会进入继承的原型对象上查找，找不到就会返回undefined。对属性和方法的搜索会一直持续到原型链的末端，通常就是Object。

如何判断一个属性是自己定义的属性，还是原型链上继承的属性呢，先通过in操作符，in操作符只要能够找到对应的方法，就会返回true；Object.hasOwnProperty()方法用于确定某个属性是否在实例上。这两个方法配合使用就可以确定属性的来源。



问题：当在原型上定义了引用类型时，该引用值会在所有的实例间共享，一旦某个实例修改了这个引用，其他所有的实例都会跟这改变；在原型链继承时，子类型实例化时不能给父类构造函数传参，也就是无法在不影响其他实例的情况下给父类构造函数传参。

```JavaScript
function sub(){
    this.color = ['red','green']
}
sub.prototype.getName = function() {
    return this.name
}
sub.prototype.hobby = ['dance','draw']

function sup() {}
sup.prototype = new sub()

let sup1 = new sup()
sup1.color.push('black')
sup1.hobby.push('sing')
console.log(sup1.color) //["red", "green", "black"]
console.log(sup1.hobby) // ["dance", "draw", "sing"]

let sup2 = new sup()
console.log(sup2.color) //["red", "green", "black"]
console.log(sup2.hobby) // ["dance", "draw", "sing"]
```



###### 盗用构造函数

> 盗用构造函数有时候也叫做对象伪装或经典继承。基本思路：在子类构造函数中调用父类构造函数。函数就是在特定上下文对象中执行代码的简单函数，可以通过call()和apply()改变this的指向，在特定的上下文对象中执行函数。

```JavaScript
function sub() {
    this.color = ['red','green']
}
function sup() { 
    // 此处this指向sup新实例，在新实例中调用sub（）
    sub.call(this)
}

let sup1 = new sup()

sup1.color.push('black')
console.log(sup1.color) //["red", "green", "black"]

let sup2 = new sup()
console.log(sup2.color) //["red", "green"]
```

这种方式必须在构造函数中定义方法，因此函数无法复用；子类也不能访问父类原型上定义的方法。

###### 组合继承

> 组合继承也叫伪经典继承，综合了原型链和盗用构造函数，将两者的优点集中起来。基本思路:使用原型链继承原型上的方法，使用盗用构造函数继承实例属性。

```JavaScript
function sub() {
this.color = ['red','green']
}
sub.prototype.hobby = ['dance','draw']

function sup() { 
sub.call(this)
}
sup.prototype = new sub()

let sup1 = new sup()
let sup2 = new sup()
sup1.color.push('black')
sup1.hobby.push('sing')

console.log(sup1.color) //["red", "green", "black"]
console.log(sup1.hobby) //["dance", "draw", "sing"]

console.log(sup2.color)  //["red", "green"]
console.log(sup2.hobby)  // ["dance", "draw", "sing"]
```

###### 原型式继承

> 

有点乏了，待会再写