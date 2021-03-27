## JavaScript--类

> ES6新引入了class关键字具有了正式定义类的能力，实际上类就是ES6中新的基础性语法糖结构，背后使用的仍然是原型和构造函数的概念。

###### 类的定义及构造函数

类的定义与函数类似，类声明和类表达式。

```JavaScript
class person {} //类声明
const person = cass {} // 类表达式
```

与函数不同之处有两点，函数声明可以提升，类不可以；函数受函数作用域限制，类受作用域限制。

```JavaScript
console.log(person)
class person {}  //undefined

{
    class person {}
}
console.log(person) //undefined
```

类的构造函数通过constructor关键字在类定义块内部创建，constructor关键字会告诉解释器在使用new操作符创建新实例时，应该调用这个函数。类的构造函数也不是必须的，不定义构造函数相当于将构造函数定义为空函数。

使用new操作符实例化类等于使用new操作符调用器构造函数。通过new操作符实例化类会执行如下操作：

- 在内存中创建一个新对象
- 这个新对象内部的prototype指针被赋值为构造函数的prototype属性，即构造函数的原型
- 构造函数内部的this被赋值为这个新对象，this指向新对象
- 执行构造函数内部代码，为新对象添加属性
- 如果构造函数返回非空对象，则返回该对象；否则返回新创建的对象

如果构造函数内有对象返回，则该对象就不会通过instanceof操作符检测出跟类有关联，因为这个对象的原型指针没有被修改。

###### 实例、原型及类成员

每个实例都对应一个唯一的成员对象，这意味着所有的成员都不会在原型上共享。

```JavaScript
class person{
	constructor() {
		this.name = new String('nick')
	}
}
let p1 = new person()
	p2 = new person()

console.log(p1.name == p2.name) //false
```

可以在类块中定义方法作为原型方法来实现实例间共享，也就是说定义在类块里的方法，实际上也就是定义在类的原型上

```JavaScript
class person{
	color() {
		console.log('red')
	}
}
let p1 = new person()
p1.color() //red
person.prototype.color() //red
```

使用static关键字可以在类上定义静态方法，静态方法通常用于执行不特定与实例的操作，可以通过类名调用。

```JavaScript
class person{
	static color() {
		console.log('red')
	}
}
person.color() //red
```

###### 继承

ES6支持单继承，使用extends关键字，可以继承任何拥有construct和原型的对象。实际上背后依然是原型链构造函数那一套。

```JavaScript
class sub{
	color() {
		console.log('red')
	}
}

class sup extends sub{}

let p1 = new sup()
p1.color() // red
console.log(p1 instanceof sub)  //true
```

派生类的方法可以通过super关键字引用他们的原型，这个关键字只能在派生类中使用，且仅限于类构造函数、实例方法和静态方法。super使用时注意的问题：

- super只能在派生类和静态方法中调用
- 不能单独使用super关键字，要么调用构造函数，要么调用静态方法
- 调用super（）会调用父类的构造函数，并将返回的实例赋值给this
- 在类的构造函数之前，不能引用this
- 如果派生类中定义了构造函数，则要么必须在其中调用super（），要么返回返回一个对象。

抽象基类是可供给其他类继承，但不会被实例化的，ES6虽然没提供专门支持这种类的语法，但通过new.target也很容易实现。new是从构造函数生成实例对象的命令，ES6为new引入了一个new.target属性，该属性一般用于构造函数之中，返回new命令作用于的那个构造函数。如果构造函数不是通过new命令或者Relect.construct（）调用的，new.tartget会返回undefined，因此这个属性可以来确定构造函数的调用方式。

```JavaScript
class subAbstract{
	constructor() {
		console.log(new.target)
		if(new.target === subAbstract) {
			throw new Error('abstract 不能被实例化')
		}
	}
}

class sup extends subAbstract{}
new sup() // 子类继承父类时   会返回子类
new subAbstract()  //new.tarhet在类内部调用时会返回类本身
```

利用这个属性还可以在抽象基类中检查，要求子类必须定义某个方法，因为原型在调用类构造函数之前就已经存在了，所以可以通过this关键字来检查。

```JavaScript
class subAbstract{
	constructor() {
		console.log(new.target)
		if(new.target === subAbstract) {
			throw new Error('abstract 不能被实例化')
		}
		if(!this.foo){
			throw new Error('foo 必须被定义')
		}
		console.log('bingo')
	}
}

class sup1 extends subAbstract{}

class sup2 extends subAbstract{
	foo(){}
}

//new sup1()
new sup2()
```

###### 类混入

> 把不同类的行为集中到一个类是一种常见的js模式，虽然es6没有显示的支持多继承，但通过现有的特性可以模拟这种行为。Object.asign()方法可以实现混入对象的行为，只有在需要混入类的行为时才有必要自己实现混入表达式，如果只是混入多个对象的属性，使用Object.asign()就可以了。
>
> 混入模式可以通过在一个表达式中连缀多个混入元素来实现，这个表达式最终会被解析成为一个可以被继承的类。譬如person类需要组合A、B、C，则需要某种机制实现B继承A，C继承B，而person再继承C，从而把A、B、C组合到这个超类中。

```JavaScript
class subAbstract{}

let FooMixin = (SuperClass) => class extends SuperClass {
	foo() {
		console.log('foo')
	}
}

let BarMixin = (SuperClass) => class extends SuperClass {
	bar() {
		console.log('bar')
	}
}

let BazMixin = (SuperClass) => class extends SuperClass {
	baz() {
		console.log('baz')
	}
}

class bus extends FooMixin(BarMixin(BazMixin(subAbstract))) {}

let b = new bus()

b.foo() //foo
b.bar() //bar
b.baz() //baz
```

类的名字可以是个可求职的表达式，BazMixin(subAbstract)