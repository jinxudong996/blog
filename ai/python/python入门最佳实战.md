最近想在学习下`langchain`，发现很多这部分的资料都是`python`版本的，就做一个入门教程，重新学习下这部分。

##### python基础

`python`也是弱类型语言，和JS一样，类型是在赋值时动态推断的。

这种弱类型语言遇到大型项目维护都是很麻烦的，`javascript`推出了`typescript`超集来做类型检查，而`python`也有`mypy`官方静态类型检查器，用法也和`typescript`非常相像，` def func(x: int) -> str: `。

最看不习惯的，还是它的缩进，明明一个大括号就能解决的事，非要搞缩进，可能看的少了。

###### 数据类型和变量

1. 整数

`python`可以处理任意大小的整数，包括负整数。遇到很大的数， 允许在数字中间以`_`分隔，因此，写成`10_000_000_000`和`10000000000`是完全一样的。 

`Python` 的整数类型（`int`）不像 C/C++/Java 等语言那样有固定位数（如 32 位或 64 位）。它可以自动扩展以存储任意大的整数。 

2. 浮点数

浮点数也就是小数，之所以称为浮点数，是因为按照科学记数法表示时，一个浮点数的小数点位置是可变的，比如，1.23x109和12.3x108是完全相等的。浮点数可以用数学写法，如`1.23`，`3.14`，`-9.01`，等等。但是对于很大或很小的浮点数，就必须用科学计数法表示，把10用e替代，1.23x109就是`1.23e9`，或者`12.3e8`，0.000012可以写成`1.2e-5`。

 3.字符串

 字符串是以单引号`'`或双引号`"`括起来的任意文本，比如`'abc'`，`"xyz"`等等 。遇到特殊字符可以使用`/`来转译。`'I\'m \"OK\"!'` 就是`I'm "OK"!`

4. 布尔值

 布尔值和布尔代数的表示完全一致，一个布尔值只有`True`、`False`两种值，要么是`True`，要么是`False` 。

5. 空值

 空值是Python里一个特殊的值，用`None`表示。`None`不能理解为`0`，因为`0`是有意义的，而`None`是一个特殊的空值。 

6. 变量

`python`申明变量不需要任何关键字，直接定义

```python
name = 'king'
print(name)
```

###### list

 list是一种有序的集合，可以随时添加和删除其中的元素。和`javascript`中的数组基本一致。

```python
mixed_list = [1, "hello", 3.14, True]

print(mixed_list)
mixed_list[0] = 2
mixed_list.append('cc')

print(mixed_list)
```

切片是操作list比较常见的做法

```python
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
 
# 提取索引 2 到 5（不包含5）的元素
print(lst[2:5])  # 输出: [2, 3, 4]
 
# 从头到索引 4（不包含4）
print(lst[:4])   # 输出: [0, 1, 2, 3]
 
# 从索引 6 到末尾
print(lst[6:])   # 输出: [6, 7, 8, 9]

```

当然切片也有第三个参数，默认就是1，比如

```python
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(lst[2:7:2])
#[2, 4, 6]
```

相当于指定间隔

###### tuple

 另一种有序列表叫元组：tuple。tuple和list非常类似，但是tuple一旦初始化就不能修改。只不过和js的`const`一样，不可变的只是变量本身，一旦应用了对象，实际上也是可变的。

```python
t = ('a', 'b', ['A', 'B'])
t[2][0] = 'X'
t[2][1] = 'Y'
print(t) 
```

###### 条件判断

这里的条件判断，编程语言都大差不差，主要还是语法的格式

```python
age = 20
if age >= 6:
    print('teenager')
elif age >= 18:
    print('adult')
else:
    print('kid')
```

在js中如果`if else`过长还有`switch case`可以简化下，只是python用`match`来做的

```python
score = 'B'
if score == 'A':
    print('score is A.')
elif score == 'B':
    print('score is B.')
elif score == 'C':
    print('score is C.')
else:
    print('invalid score.')
```

用`match`可以改写成

```python
score = 'B'

match score:
    case 'A':
        print('score is A.')
    case 'B':
        print('score is B.')
    case 'C':
        print('score is C.')
    case _: # _表示匹配到其他任何情况
        print('score is ???.')
```

###### 循环

`for in` 循环

```python
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)
```

`while循环`

```python
sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)
```

###### dict和set

dict在js中就是map， 使用键-值（key-value）存储，具有极快的查找速度 

```python
d = {"a": 1, "b": 2}
d["c"] = 3       # 添加/修改
del d["a"]       # 删除键
"b" in d         # 检查键是否存在
d.keys()         # 获取所有键
d.values()       # 获取所有值
d.items()        # 获取键值对
```

而set和dict类似，也是一组key的集合， 不存储value，但是key不能重复 ，这里和js中的set也很相似

```python
s = {1, "hello", (1, 2)}  # 合法
# s = {[1, 2]}  # 报错：列表不可哈希
```

```python
s = {1, 2, 3}
s.add(4)       # 添加元素
s.remove(2)    # 删除元素（不存在时抛出 KeyError）
s.discard(5)   # 删除元素（不存在时不报错）
s.pop()        # 随机移除并返回一个元素
s.clear()      # 清空集合
2 in s         # 检查元素是否存在
```



##### 函数

python内置了许多工具方法，比如数学计算的`abs()`、`max()`

```python
print(abs(-20))
print(max(2, 3, 1, -5))
```

还有内置的一些类型转换方法

```python
int('123')
float('12.34')
str(100)
```

自定义函数的话，可以通过`def`关键字来申明

```python
def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x

print(my_abs(-99))
```

也可以和js一样，给参数指定默认值

```python
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
```

python还内置了map、reduce等方法，用于遍历迭代器的，用法和js稍有区别，

比如`map()`函数接收两个参数，一个是函数，一个是`Iterable`，`map`将传入的函数依次作用到序列的每个元素，并把结果作为新的`Iterator`返回。 

```plain
r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
```

 `reduce`把一个函数作用在一个序列`[x1, x2, x3, ...]`上，这个函数必须接收两个参数，`reduce`把结果继续和序列的下一个元素做累积计算 

```python
reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
```

这些函数作用和js基本一致，只是在用法上稍有差别。

##### 模块

可以将常用功能封装成模块，方便在不同文件中复用。

比如新建`mymodule.py`

```python
# mymodule.py
 
def greet(name):
    return f"Hello, {name}!"
 
PI = 3.14159
```

就可以通过`import`来导入整个模块

```python
import mymodule
 
print(mymodule.greet("Alice"))  # 输出: Hello, Alice!
print(mymodule.PI)  # 输出: 3.14159
```

也可以导入特定内容

```python
from mymodule import greet, PI
 
print(greet("Bob"))  # 输出: Hello, Bob!
print(PI)  # 输出: 3.14159
```

管理一些第三方模块，也可以通过`pip`，用法和`npm`基本一致

