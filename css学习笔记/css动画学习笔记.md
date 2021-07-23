css动画学习笔记

css3的几个新特性，animation，transition，transform，translate也只是大概看过些文档，以前也做过一些小案例，平时用的也不多，前段时间要做个侧边栏，要求鼠标悬浮然后划出，滑到头之后展示个图片，一下子想不起来这些api的用法，现在梳理下。

###### 1.animation

MDN上是这样定义animation属性的：

>   **CSS transitions** 提供了一种在更改CSS属性时控制动画速度的方法。 其可以让属性变化成为一个持续一段时间的过程，而不是立即生效的。比如，将一个元素的颜色从白色改为黑色，通常这个改变是立即生效的，使用 CSS transitions 后该元素的颜色将逐渐从白色变为黑色，按照一定的曲线速率变化。这个过程可以自定义。 

animation是属性的简写，接下来一一学习。

###### 1.1 animation-name

该属性用于指定@keyframes动画的名称，，定义关键帧需要使用@keyframes规则 ，样式快可以使用from...to结构，也可以使用百分比来定义。

###### 1.2 animation-duration设置动画的持续时间

```css
<div class="box"></div>
<!--css代码-->
.box{
    width:100px;
    height:100px;
    animation-name:big;
    animation-duration:3s;
    border:1px solid red;
}
@keyframes big{
    0%{width:100px;height:100px;}
    50%{width:130px;height:130px;}
    100%{width:150px;height:150px;}
}
```

###### 1.3 animation-timing-function 设置动画的过渡类型

常用的值有

​	linear:动画匀速

​	ease:默认值，动画先低速开始，然后加快，在结束前变慢

​	ease-in:动画以低速开始

​	ease-out:动画以低速结束

​	ease-in-out:动画以低速开始和结束

​	cubic-bezie(n,n,n):在cubic-bezier函数中自己的值

###### 1.4 animation-delay 设置动画延迟时间

###### 1.5 animation-iteration-count 设置动画在循环中是否反向运动

​	常用的值有

​	normal:默认值，正常播放

​	reverse：动画反向播放

​	alternate：动画奇数正常播放，偶数反向播放

​	alternate-reverse：动画奇数反向播放，偶数正向播放

​	initial：设置该属性为默认值

​	inherit：从父元素继承

###### 1.6 animation-play-state：设置动画的状态，控制动画的播放与暂停

###### 1.7 **`animation-fill-mode`** 设置CSS动画在执行之前和之后如何将样式应用于其目标 

​	none：默认值，当动画未执行时，动画将不会把任何样式应用于目标，而是已经赋予该元素的css规则来显示该元素

​	forwards：将保留执行期间遇到的最后一个关键帧的计算值

​	ackards：动画在用应用于目标时立即应用第一个关键帧中定义的值，在animation-delay期间保留此值

​	both：动画将遵循forwards和backwards的规则，从两个方向上扩展动画属性。

