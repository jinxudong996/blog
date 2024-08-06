1.  canvas画布  是h5新增的一个DOM元素，可以显示二维和三位的图像
2. 阿萨德

##### webgl入门简介

webgl是一种3D绘图协议，衍生于OpenGL ES2.0，可以结合Html5和JavaScript在网页上绘制和渲染二维三维图形。

优势：

1. 内嵌在浏览器中，不需要安装插件
2. 只需要一个文本编辑器和浏览器，就可以编写三维图像程序
3. 学习和使用比较简单

着色器就是让开发者自己去编写一段程序，用来代替固定渲染管线，来处理图像的渲染。

顶点着色器：用来描述定点的特性，通过计算获取位置信息，顶点是指二维三维空间中的一个点，可以理解为一个个坐标

片元着色器，进行逐片元处理程序，通过计算获取颜色信息。片元可以理解为一个个像素





WebGL（Web Graphics Library）是一种基于 JavaScript API 的图形渲染技术，它允许在网页上使用硬件加速的 3D 图形和可视化效果。

WebGL 是由 Khronos Group 开发和维护的，它基于 OpenGL ES（OpenGL for Embedded Systems）标准，将其适配到了 Web 环境中。通过使用 WebGL，开发者可以在网页上创建交互式的 3D 场景、动画和效果，而无需使用插件或其他额外的软件。

WebGL 利用了计算机的图形处理单元（GPU）来进行高性能的图形渲染。它提供了一组底层的 API，允许开发者直接操作图形渲染管线，包括顶点处理、片元处理、纹理映射、着色器编程等。通过编写自定义的着色器程序，开发者可以实现各种复杂的图形效果和渲染技术。

WebGL 的主要特点包括：

1. 硬件加速：WebGL 利用 GPU 进行图形渲染，可以实现高性能的 3D 图形和动画效果。

2. 跨平台：WebGL 可以在各种现代的 Web 浏览器上运行，包括桌面浏览器和移动设备浏览器。

3. 开放标准：WebGL 是一个开放的标准，由 Khronos Group 维护，具有广泛的支持和社区参与。

4. 与 Web 技术集成：WebGL 可以与其他 Web 技术（如 HTML、CSS、JavaScript）无缝集成，实现丰富的交互和用户体验。

WebGL 在许多领域有广泛的应用，包括游戏开发、数据可视化、虚拟现实、建筑设计等。它为开发者提供了强大的工具和能力，使他们能够在网页上创建出令人惊叹的图形和视觉效果。

###### 初识webgl

使用webgl首先需要一个canvas元素，接下来写一个简单的下例子来认识下webgl：

```javascript
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>webgl</title>
</head>
<body onload="main()">
  <canvas id="glcanvas" width="640" height="480">
    你的浏览器似乎不支持或者禁用了 HTML5 <code>&lt;canvas&gt;</code> 元素。
  </canvas>
</body>

<script>
  function main() {
  const canvas = document.querySelector("#glcanvas");
  // 初始化 WebGL 上下文
  const gl = canvas.getContext("webgl");

  // 确认 WebGL 支持性
  if (!gl) {
    alert("无法初始化 WebGL，你的浏览器、操作系统或硬件等可能不支持 WebGL。");
    return;
  }

  // 使用完全不透明的黑色清除所有图像
  gl.clearColor(0.0, 0.0, 0.0, 1.0);
  // 用上面指定的颜色清除缓冲区
  gl.clear(gl.COLOR_BUFFER_BIT);
}
</script>
</html>
```

上面代码会在指定位置绘制一个黑色的区域。代码也比较简单，首先获取一个canvas引用， 然后调用[getContext](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLCanvasElement/getContext) 函数并向它传递 `"webgl"` 参数，来尝试获取[WebGLRenderingContext](https://developer.mozilla.org/zh-CN/docs/Web/API/WebGLRenderingContext)；如果浏览器不支持 webgl, `getContext` 将会返回 `null`，我们就可以显示一条消息给用户然后退出。 



###### 创建2D内容



###### 着色器



###### 动画



###### 创建3D内容



###### 使用纹理贴图



###### 灯光



###### 动画纹理贴图















