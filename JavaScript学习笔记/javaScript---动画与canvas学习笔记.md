####  requestAnimationFrame() 

##### 背景

以前，在 JavaScript 中创建动画基本上就是使用 setInterval()来控制动画的执行 ， 这种定时动画的问题在于无法准确知晓循环之间的延时。定时间隔必须足够短，这样才能让不同的 动画类型都能平滑顺畅，但又要足够长，以便产生浏览器可以渲染出来的变化。

一般计算机显示器的屏 幕刷新率都是 60Hz，基本上意味着每秒需要重绘 60 次。大多数浏览器会限制重绘频率，使其不超出屏 幕的刷新率，这是因为超过刷新率，用户也感知不到。 因此，实现平滑动画最佳的重绘间隔为 1000 毫秒/60，大约 17 毫秒。以这个速度重绘可以实现最平 滑的动画，因为这已经是浏览器的极限了。如果同时运行多个动画，可能需要加以限流，以免 17 毫秒 的重绘间隔过快，导致动画过早运行完。 

虽然使用 setInterval()的定时动画比使用多个 setTimeout()实现循环效率更高，但也不是没 有问题。无论 setInterval()还是 setTimeout()都是不能保证时间精度的。作为第二个参数的延时 只能保证何时会把代码添加到浏览器的任务队列，不能保证添加到队列就会立即运行。如果队列前面还 有其他任务，那么就要等这些任务执行完再执行。简单来讲，这里毫秒延时并不是说何时这些代码会执 行，而只是说到时候会把回调加到任务队列。如果添加到队列后，主线程还被其他任务占用，比如正在 处理用户操作，那么回调就不会马上执行 

##### 用法

ES6新增了一个 requestAnimationFrame方法，用以通知浏览器某些 JavaScript 代码要执行动画了。这样浏览器就可以在运行某些代码后进行适当的优化。 该方法接收一个参数，此参数是一个要在重绘屏幕前调用的函数。 函数就是修改 DOM 样式以反映下一次重绘有什么变化的地方 。

```javascript
function updateProgress() {
	var div = document.getElementById("status");
	div.style.width = (parseInt(div.style.width, 10) + 5) + "%";
	if (div.style.left != "100%") {
 		requestAnimationFrame(updateProgress);
	}
}
requestAnimationFrame(updateProgress); 
```

因为 requestAnimationFrame()只会调用一次传入的函数，所以每次更新用户界面时需要再手 动调用它一次 。

与 setTimeout()类似，requestAnimationFrame()也返回一个请求 ID，可以用于通过另一个 方法 cancelAnimationFrame()来取消重绘任务 

```javascript
let requestID = window.requestAnimationFrame(() => {
	console.log('Repaint!');
});
window.cancelAnimationFrame(requestID);
```

##### 节流

[节流与防抖](https://juejin.cn/post/7030787304696315918)主要通过定时器来完成的，这里也可以使用requestAnimationFrame函数配合定时器来完成一个防抖函数，计时器可以限制实际的操作执行间隔，而 requestAnimationFrame 控制在浏览器的哪个渲染周期中执行。 

```javascript
let enabled = true;
function expensiveOperation() {
	console.log('Invoked at', Date.now());
}
window.addEventListener('scroll', () => {
	if (enabled) {
		enabled = false;
        window.requestAnimationFrame(expensiveOperation);
        window.setTimeout(() => enabled = true, 50);
	}
});
```



#### canvas

使用`<canvas>`标签创建画布，通过`width`、`height`设置画布大小，使用`getContext`方法获取对绘图上下文的引用。 对于平面图形，需要给这个方法传入参数"2d"，表示要获取 2D 上下文对象： 

```html
<canvas id="drawing" width="200" height="200"></canvas>

let drawing = document.getElementById("drawing");
let context = drawing.getContext("2d");
```

##### 设置2D绘图上下文

 2D 绘图上下文提供了绘制 2D 图形的方法，包括矩形、弧形和路径。2D 上下文的坐标原点(0, 0)在 元素的左上角。所有坐标值都相对于该点计算，因此 x 坐标向右增长，y 坐标向下增长。默认 情况下，width 和 height 表示两个方向上像素的最大值。 

###### 绘制矩形

矩形是唯一一个可以直接在 2D 绘图上下文中绘制的形状。与绘制矩形相关的方法有 3 个： fillRect()、strokeRect()和 clearRect()。这些方法都接收 4 个参数：矩形 x 坐标、矩形 y 坐标、 矩形宽度和矩形高度。这几个参数的单位都是像素。 

```javascript
let drawing = document.getElementById("drawing");
let context = drawing.getContext("2d");

context.fillStyle = "#ff0000";
context.fillRect(10, 10, 50, 50);

context.fillStyle = "rgba(0,0,255,0.5)";
context.fillRect(30, 30, 50, 50);
```

以上代码先将 fillStyle 设置为红色并在坐标点(10, 10)绘制了一个宽高均为 50 像素的矩形。接 着，使用 rgba()格式将 fillStyle 设置为半透明蓝色，并绘制了另一个与第一个部分重叠的矩形。 结果就是可以透过蓝色矩形看到红色矩形。

```javascript
context.strokeStyle = "#ff0000";
context.strokeRect(10, 10, 50, 50);
// 绘制半透明蓝色轮廓的矩形
context.strokeStyle = "rgba(0,0,255,0.5)";
context.strokeRect(30, 30, 50, 50); 
```

 strokeRect()方法使用通过 strokeStyle 属性指定的颜色绘制矩形轮廓 。

```javascript
// 绘制红色矩形
context.fillStyle = "#ff0000";
context.fillRect(10, 10, 50, 50);
// 绘制半透明蓝色矩形
context.fillStyle = "rgba(0,0,255,0.5)";
context.fillRect(30, 30, 50, 50);
// 在前两个矩形重叠的区域擦除一个矩形区域
context.clearRect(40, 40, 10, 10); 
```

 使用 clearRect()方法可以擦除画布中某个区域。



###### 绘制路径

要绘制 路径，必须首先调用 beginPath()方法以表示要开始绘制新路径。 主要有以下方法：

  arc(x, y, radius, startAngle, endAngle, counterclockwise)：以坐标(x, y)为圆 心，以 radius 为半径绘制一条弧线，起始角度为 startAngle，结束角度为 endAngle（都是 弧度）。最后一个参数 counterclockwise 表示是否逆时针计算起始角度和结束角度（默认为 顺时针）。 

 arcTo(x1, y1, x2, y2, radius)：以给定半径 radius，经由(x1, y1)绘制一条从上一点 到(x2, y2)的弧线。 

 bezierCurveTo(c1x, c1y, c2x, c2y, x, y)：以(c1x, c1y)和(c2x, c2y)为控制点， 绘制一条从上一点到(x, y)的弧线（三次贝塞尔曲线）。 

 lineTo(x, y)：绘制一条从上一点到(x, y)的直线。  moveTo(x, y)：不绘制线条，只把绘制光标移动到(x, y)。 

 quadraticCurveTo(cx, cy, x, y)：以(cx, cy)为控制点，绘制一条从上一点到(x, y) 的弧线（二次贝塞尔曲线）。 

 rect(x, y, width, height)：以给定宽度和高度在坐标点(x, y)绘制一个矩形。

```javascript
// 创建路径
context.beginPath();
// 绘制外圆
context.arc(100, 100, 99, 0, 2 * Math.PI, false);
// 绘制内圆
context.moveTo(194, 100);
context.arc(100, 100, 94, 0, 2 * Math.PI, false);
// 绘制分针
context.moveTo(100, 100);
context.lineTo(100, 15);
// 绘制时针
context.moveTo(100, 100);
context.lineTo(35, 100);
// 描画路径
context.stroke();
```

使用 arc()绘制了两个圆形，一个外圆和一个内圆，以构成表盘的边框。外圆半径 99 像 素，原点为(100,100)，也就是画布的中心。要绘制完整的圆形，必须从 0 弧度绘制到 2π 弧度（使用数 学常量 Math.PI）。而在绘制内圆之前，必须先把路径移动到内圆上的一点，以避免绘制出多余的线条。 第二次调用 arc()时使用了稍小一些的半径，以呈现边框效果。然后，再组合运用 moveTo()和 lineTo() 分别绘制分针和时针。最后一步是调用 stroke()， 

###### 绘制文本

此2D绘图上下文还提供了绘制文本的方法，即fillText() 和 strokeText()。这两个方法都接收 4 个参数：要绘制的字符串、x 坐标、y 坐标和可选的最大像素宽度 。

设置文本的属性主要有三个：

- font， 以 CSS 语法指定的字体样式、大小、字体族 
- textAlign， 指定文本的对齐方式 
- textBaseLine， 指定文本的基线 

```javascript
// 创建路径
context.beginPath();
// 绘制外圆
context.arc(100, 100, 99, 0, 2 * Math.PI, false);
// 绘制内圆
context.moveTo(194, 100);
context.arc(100, 100, 94, 0, 2 * Math.PI, false);
// 绘制分针
context.moveTo(100, 100);
context.lineTo(100, 15);
// 绘制时针
context.moveTo(100, 100);
context.lineTo(35, 100);
// 描画路径
context.stroke();

context.font = "bold 14px Arial";
context.textAlign = "center";
context.textBaseline = "middle";
context.fillText("12", 100, 20);
```

###### 变换

2D 绘图上下文支持所有常见的绘制变换。

- rotate， 围绕原点把图像旋转 angle 弧度 
-  scale(scaleX, scaleY)：通过在 x 轴乘以 scaleX、在 y 轴乘以 scaleY 来缩放图像。scaleX 和 scaleY 的默认值都是 1.0 
-  translate(x, y)：把原点移动到(x, y)。执行这个操作后，坐标(0, 0)就会变成(x, y)。 
-  transform(m1_1, m1_2, m2_1, m2_2, dx, dy)：通过矩阵乘法直接修改矩阵。 
-  setTransform(m1_1, m1_2, m2_1, m2_2, dx, dy)：把矩阵重置为默认值，再以传入的 参数调用 transform()。 

```javascript
// 创建路径
context.beginPath();
// 绘制外圆
context.arc(100, 100, 99, 0, 2 * Math.PI, false);
// 绘制内圆
context.moveTo(194, 100);
context.arc(100, 100, 94, 0, 2 * Math.PI, false);
// 移动原点到表盘中心
context.translate(100, 100);
// 旋转表针
context.rotate(1);
// 绘制分针
context.moveTo(0, 0);
context.lineTo(0, -85);
// 绘制时针
context.moveTo(0, 0);
context.lineTo(-65, 0);
// 描画路径
context.stroke();
```
