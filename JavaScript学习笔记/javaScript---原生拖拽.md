> **HTML 拖放（Drag and Drop）**接口使应用程序能够在浏览器中使用拖放功能。例如，用户可使用鼠标选择可拖拽（*draggable*）元素，将元素拖拽到可放置（*droppable*）元素，并释放鼠标按钮以放置这些元素。拖拽操作期间，会有一个可拖拽元素的半透明快照跟随着鼠标指针 

##### api介绍

首先要介绍一个全局属性， [draggable](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Global_attributes#attr-draggable) ，指示是否可以拖动元素，a标签和img标签默认都是设置的`draggable：true`，表明该元素是可拖拽的。

拖拽是一个事件，自然绑定了很多事件处理程序，接下来一一介绍：

- ondrag，当拖拽元素或者选中的文本时触发

- ondraggend，当拖拽操作结束时触发，松开鼠标或者敲Esc键。

  ```html
  <div class="txt" id="txt">
  	所有的文字都可拖拽。
  	<p draggable="true">此段文字设置了属性draggable="true"</p>  
  </div>
  
  var dragSrc = document.getElementById('txt')
  dragSrc.ondrag = handle_drag
  dragSrc.ondragend = handle_end
  
  function handle_drag(e){
  	console.log(e.target)
  }
  
  function handle_end(e){
  	console.log(e)
  	console.log("####################")
  }
  ```

- ondragenter，当拖拽元素或选中的文本得到一个可释放目标时触发

- ondragexit， 当元素变得不再是拖拽操作的选中目标时触发。 

- ondragleave，当拖拽元素或选中的文本离开一个可释放目标时触发。 

- ondragover， 当元素或选中的文本被拖到一个可释放目标上时触发（每100毫秒触发一次）。 

  ```javascript
  target.ondragenter = handle_enter
  target.ondragleave = handle_ondragleave、
  
  function handle_enter(e) {
  	e.preventDefault()
  	console.log('handle_enter-当元素进入目的地时触发')
  }
  function handle_ondragleave(e){
  	console.log('handle_enter-当元素离开目的地时触发')
  }
  ```

- ondragstart， 当用户开始拖拽一个元素或选中的文本时触发 

- ondrop ，当元素或选中的文本在可释放目标上被释放时触发 

总结一下：

- 被拖动元素：ondragstart、ondrop 、ondraggend、ondrag
- 放置区元素：ondragleave、ondragover、ondragenter、ondrop 

##### 基本步骤

- 确定可拖拽目标

  给元素添加`draggable`属性

- 定义拖拽数据

  每一个事件处理程序都有一个参数，这个就是`DragEvent`，每一个`DragEvent`都有一个`dataTransfer`属性，其中保存着事件的数据，使用`setData()`方法为拖拽数据添加一个项，每个数据项都是一个MIME类型的字符串， 支持拖动各种类型的数据，包括纯文本、URL、HTML 代码、文件等。 

  ```javascript
  event.dataTransfer.setData("text/plain", "This is text to drag");
  event.dataTransfer.setData("text/plain", "https://www.mozilla.org");
  event.dataTransfer.mozSetDataAt("application/x-moz-file", file, 0);
  ```

- 定义拖拽图像

  拖拽过程中，浏览器会在鼠标旁显示一张默认图片，可以通过 [`setDragImage()`](https://developer.mozilla.org/zh-CN/docs/Web/API/DataTransfer/setDragImage) 方法自定义。

  ```javascript
  function dragstart_handler(ev) {
    // Create an image and then use it for the drag image.
    // NOTE: change "example.gif" to a real image URL or the image
    // will not be created and the default drag image will be used.
    var img = new Image();
    img.src = 'example.gif';
    ev.dataTransfer.setDragImage(img, 10, 10);
  }
  ```

  

- 定义拖拽效果

   [`dropEffect`](https://developer.mozilla.org/zh-CN/docs/Web/API/DataTransfer/dropEffect) 属性用来控制拖放操作中用户给予的反馈。它会影响到拖拽过程中浏览器显示的鼠标样式。 

  有三个效果可以定义：

  - copy，表明被拖拽的数据将从它原本的位置拷贝到目标的位置
  - move， 表明被拖拽的数据将被移动 
  - link， 表明在拖拽源位置和目标位置之间将会创建一些关系表格或是连接 

  ```javascript
  function dragstart_handler(ev) {
    ev.dataTransfer.dropEffect = "copy";
  }
  ```

  

- 定义一个放置区

  当拖拽一个项目到 HTML 元素中时，浏览器默认不会有任何响应。想要让一个元素变成可释放区域，该元素必须设置 [`ondragover` (en-US)](https://developer.mozilla.org/en-US/docs/Web/API/GlobalEventHandlers/ondragover) 和 [`ondrop`](https://developer.mozilla.org/zh-CN/docs/Web/API/GlobalEventHandlers/ondrop) 事件处理程序属性 。

  ```javascript
  function dragover_handler(ev) {
   ev.preventDefault();
   //...
  }
  function drop_handler(ev) {
   ev.preventDefault();
   //...
  }
  ```

##### 例子

实现图片拖放的小例子，通过切换class来实现图片的展示。

```html
<!DOCTYPE html>
<html>
<head>
	<title>图片拖放</title>
	<meta charset="utf-8">
	<style type="text/css">
		body {
		  background-color: darksalmon;
		}

		.draggable {
		  background-image: url('http://source.unsplash.com/random/150x150');
		  position: relative;
		  height: 150px;
		  width: 150px;
		  top: 5px;
		  left: 5px;
		  cursor: pointer;
		}

		.droppable {
		  display: inline-block;
		  height: 160px;
		  width: 160px;
		  margin: 10px;
		  border: 3px salmon solid;
		  background-color: white;
		}

		.dragging {
		  border: 4px yellow solid;
		}

		.drag-over {
		  background-color: #f4f4f4;
		  border-style: dashed;
		}

		.invisible {
		  display: none;
		}
	</style>
</head>
<body>
<div class="droppable">
	<div class="draggable" draggable="true"></div>
</div>
<div class="droppable"></div>
<div class="droppable"></div>
<div class="droppable"></div>
<div class="droppable"></div>

<script type="text/javascript">
	// 查询draggable和droppable
const draggable = document.querySelector('.draggable');
const droppables = document.querySelectorAll('.droppable');

// 监听draggable的相关事件
draggable.addEventListener('dragstart', dragStart);
draggable.addEventListener('dragend', dragEnd);

function dragStart() {
	setTimeout(() => {
    this.className = 'invisible';
  }, 0);
	
}

function dragEnd() {
	
  this.className = 'draggable';
}

// 监听droppable的相关事件
for (const droppable of droppables) {
  droppable.addEventListener('dragover', dragOver);
  droppable.addEventListener('dragleave', dragLeave);
  droppable.addEventListener('dragenter', dragEnter);
  droppable.addEventListener('drop', dragDrop);
}

function dragOver(e) {
  e.preventDefault();
}

function dragEnter(e) {
  e.preventDefault();
  this.className += ' drag-over';
}

function dragLeave(e) {
  this.className = 'droppable';
}

function dragDrop(e) {
  this.className = 'droppable';
  this.append(draggable);
}
</script>

</body>
</html>
```
