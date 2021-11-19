#### 盒模型

>  完整的 CSS 盒模型应用于块级盒子，内联盒子只使用盒模型中定义的部分内容。模型定义了盒的每个部分 —— margin, border, padding, and content —— 合在一起就可以创建我们在页面上看到的内容。为了增加一些额外的复杂性，有一个标准的和替代（IE）的盒模型。 

![79178-12f8c9590705a099](C:\Users\Thomas东\Desktop\79178-12f8c9590705a099.png)

可以通过`box-sizing`属性来设置盒模型种类，改属性有两个值：

- `box-sizing`:`box-sizing` 默认值，标准盒子模型。 [`width`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/width) 与 [`height`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/height) 只包括内容的宽和高， 不包括边框（border），内边距（padding），外边距（margin）。注意: 内边距、边框和外边距都在这个盒子的外部。 比如说，`.box {width: 350px; border: 10px solid black;}` 在浏览器中的渲染的实际宽度将是 370px。 
  尺寸计算公式：`width` = 内容的宽度，`height` = 内容的高度
- `box-sizing`:` border-box`  [`width`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/width) 和 [`height`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/height) 属性包括内容，内边距和边框，但不包括外边距。这是当文档处于 Quirks模式 时Internet Explorer使用的[盒模型](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Box_Model/Introduction_to_the_CSS_box_model)。注意，填充和边框将在盒子内 , 例如, `.box {width: 350px; border: 10px solid black;}` 导致在浏览器中呈现的宽度为350px的盒子。内容框不能为负，并且被分配到0，使得不可能使用border-box使元素消失。 尺寸计算公式：`width` = border + padding + 内容的宽度，`height` = border + padding + 内容的高度。

#### BFC

>  **块格式化上下文（Block Formatting Context，BFC）** 是Web页面的可视CSS渲染的一部分，是块盒子的布局过程发生的区域，也是浮动元素与其他元素交互的区域。 

> 具有 BFC 特性的元素可以看作是隔离了的独立容器，容器里面的元素不会在布局上影响到外面的元素，并且 BFC 具有普通容器所没有的一些特性。通俗一点来讲，可以把 BFC 理解为一个封闭的大箱子，箱子内部的元素无论如何翻江倒海，都不会影响到外部。

出发BFC的条件：

- 根元素（`）`
- 浮动元素（元素的 [`float`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/float) 不是 `none`）
- 绝对定位元素（元素的 [`position`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/position) 为 `absolute` 或 `fixed`）
- 行内块元素（元素的 [`display`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/display) 为 `inline-block`）
- 表格单元格（元素的 [`display`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/display) 为 `table-cell`，HTML表格单元格默认为该值）
- 表格标题（元素的 [`display`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/display) 为 `table-caption`，HTML表格标题默认为该值）
- 匿名表格单元格元素（元素的 [`display`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/display) 为 `table、``table-row`、 `table-row-group、``table-header-group、``table-footer-group`（分别是HTML table、row、tbody、thead、tfoot 的默认属性）或 `inline-table`）
- [`overflow`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/overflow) 计算值(Computed)不为 `visible` 的块元素
- [`display`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/display) 值为 `flow-root` 的元素
- [`contain`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/contain) 值为 `layout`、`content `或 paint 的元素
- 弹性元素（[`display`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/display) 为 `flex` 或 `inline-flex `元素的直接子元素）
- 网格元素（[`display`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/display) 为 `grid` 或 `inline-grid` 元素的直接子元素）
- 多列容器（元素的 [`column-count`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/column-count) 或 [`column-width` (en-US)](https://developer.mozilla.org/en-US/docs/Web/CSS/column-width) 不为 `auto，包括 ``column-count` 为 `1`）
- `column-span` 为 `all` 的元素始终会创建一个新的BFC，即使该元素没有包裹在一个多列容器中（[标准变更](https://github.com/w3c/csswg-drafts/commit/a8634b96900279916bd6c505fda88dda71d8ec51)，[Chrome bug](https://bugs.chromium.org/p/chromium/issues/detail?id=709362)）。

##### BFC特性及应用：

######  **1. 同一个 BFC 下外边距会发生折叠** 

​	因为两个 div 元素都处于同一个 BFC 容器下 (这里指 body 元素) 所以第一个 div 的下边距和第二个 div 的上边距	发生了重叠，我们可以理解为一	种规范，如果想要避免外边距的重叠，可以将其放在不同的 BFC 容器中。

```html
<!DOCTYPE html>
<html>
<head>
	<title>bfc-下边距重叠</title>
	<meta charset="utf-8">
	<style type="text/css">
		.box{
			overflow: hidden;
		}
		p{
			width:100px;
			height:100px;
			margin:100px;
			border:1px solid red;
		}
	</style>
</head>
<body>
<div class="box">
	<p></p>
</div>
<div class="box">
	<p></p>
</div>
</body>
</html>
```



######  **2. BFC 可以包含浮动的元素（清除浮动）** 	

```
<!DOCTYPE html>
<html>
<head>
	<title>bfc-清除浮动</title>
	<meta charset="utf-8">
	<style type="text/css">

	</style>
</head>
<body>
<div style="border: 1px solid #000;overflow: hidden:hidden">
    <div style="width: 100px;height: 100px;background: #eee;float: left;"></div>
</div>
</body>
</html>
```

######  **3. BFC 可以阻止元素被浮动元素覆盖** 

```html
<!DOCTYPE html>
<html>
<head>
	<title>bfc-与浮动元素等高</title>
	<meta charset="utf-8">
	<style type="text/css">

	</style>
</head>
<body>
<div style="height: 100px;width: 100px;float: left;background: lightblue">我是一个左浮动的元素</div>
<div style="width: 200px; height: 200px;background: #eee;overflow: hidden;">我是一个没有设置浮动, 
也没有触发 BFC 元素, width: 200px; height:200px; background: #eee;</div>
</body>
</html>
```

#### position

> 定位是一个相当复杂的话题，所以我们深入了解代码之前，让我们审视一下布局理论，并让我们了解它的工作原理。
>
> 首先，围绕元素内容添加任何内边距、边界和外边距来布置单个元素盒子——这就是 [盒模型](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model) ，我们前面看过。 默认情况下，块级元素的内容宽度是其父元素的宽度的100％，并且与其内容一样高。内联元素高宽与他们的内容高宽一样。您不能对内联元素设置宽度或高度——它们只是位于块级元素的内容中。 如果要以这种方式控制内联元素的大小，则需要将其设置为类似块级元素 `display: block;`。
>
> 这只是解释了单个元素，但是元素相互之间如何交互呢？ **正常的布局流**（在布局介绍文章中提到）是将元素放置在浏览器视口内的系统。默认情况下，块级元素在视口中垂直布局——每个都将显示在上一个元素下面的新行上，并且它们的外边距将分隔开它们。
>
> 内联元素表现不一样——它们不会出现在新行上；相反，它们互相之间以及任何相邻（或被包裹）的文本内容位于同一行上，只要在父块级元素的宽度内有空间可以这样做。如果没有空间，那么溢流的文本或元素将向下移动到新行。
>
>  如果两个相邻元素都在其上设置外边距，并且两个外边距接触，则两个外边距中的较大者保留，较小的一个消失——这叫[外边距折叠](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Box_Model/Mastering_margin_collapsing), 我们之前也遇到过。 

>  定位的整个想法是允许我们覆盖上面描述的基本文档流行为，以产生有趣的效果。如果你想稍微改变布局中一些盒子的位置，使它们的默认布局流程位置稍微有点古怪，不舒服的感觉呢？定位是你的工具。或者，如果您想要创建一个浮动在页面其他部分顶部的UI元素，并且/或者始终停留在浏览器窗口内的相同位置，无论页面滚动多少？定位使这种布局工作成为可能。 

position一共有五个值：

- static 静态定位， 静态定位是每个元素获取的默认值——它只是意味着“将元素放入它在文档布局流中的正常位置 
- relative 相对定位, 依赖top, right, bottom, left 等属性相对于该对象在标准文档流中的位置进行偏移，同时可通过z-index定义层叠关系。 
- absolute 绝对定位，对象脱离标准文档流，使用top, right, bottom, left 等属性进行绝对定位（相对于static定位以外的第一个父元素进行绝对定位） 同时可通过z-index定义层叠关系 
- fixed 固定定位，对象脱离标准文档流，使用top, right, bottom, left 等属性进行绝对定位（相对于浏览器窗口进行绝对定位）同时可通过z-index定义层叠关系。

#### flex布局



[阮一峰大佬文章链接]: https://www.ruanyifeng.com/blog/2015/07/flex-grammar.html

>  Flexible Box 模型，通常被称为 flexbox，是一种一维的布局模型。它给 flexbox 的子元素之间提供了强大的空间分布和对齐能力 

flex容器默认存在两根轴，水平的主轴和垂直的交叉轴。

容器属性有六个值：

- felx-direction

  设置主轴的排列方向

  ```css
  .box {
    flex-direction: row | row-reverse | column | column-reverse;
  }
  ```

- felx-wrap

  设置在主轴方向排列的项目如何换行

  ```css
  .box{
    flex-wrap: nowrap | wrap | wrap-reverse;
  }
  ```

- flex-flow

  flex-direction和flex-wrap简写。

- justify-content

  定义属性在主轴的对齐方式

  ```css
  .box {
    justify-content: flex-start | flex-end | center | space-between | space-around;
  }
  ```

  ![bg2015071010](C:\Users\Thomas东\Desktop\bg2015071010.png)

- align-items

   属性定义项目在交叉轴上如何对齐。

  ```css
  .box {
    align-items: flex-start | flex-end | center | baseline | stretch;
  }
  ```

  ![bg2015071011](C:\Users\Thomas东\Desktop\bg2015071011.png)

- align-content

   属性定义了多根轴线的对齐方式。如果项目只有一根轴线，该属性不起作用 

  ```css
  .box {
    align-content: flex-start | flex-end | center | space-between | space-around | stretch;
  }
  ```

项目属性有六个值：

- order

   属性定义项目的排列顺序。数值越小，排列越靠前，默认为0 

  ```css
  .item {
    order: <integer>;
  }
  ```

- flex-grow

   属性定义项目的放大比例，默认为0，即如果存在剩余空间，也不放大 

  ```css
  .item {
    flex-grow: <number>; /* default 0 */
  }
  ```

- flex-shrink

   属性定义了项目的缩小比例，默认为1，即如果空间不足，该项目将缩小 

  ```css
  .item {
    flex-shrink: <number>; /* default 1 */
  }
  ```

- flex-basis

   属性定义了在分配多余空间之前，项目占据的主轴空间（main size）。浏览器根据这个属性，计算主轴是否有多余空间。它的默认值为auto，即项目的本来大小 

  ```css
  .item {
    flex-basis: <length> | auto; /* default auto */
  }
  ```

- flex

   属性是`flex-grow`, `flex-shrink` 和 `flex-basis`的简写 

- align-self

   `align-self`属性允许单个项目有与其他项目不一样的对齐方式，可覆盖`align-items`属性。默认值为`auto`，表示继承父元素的`align-items`属性，如果没有父元素，则等同于`stretch`。 