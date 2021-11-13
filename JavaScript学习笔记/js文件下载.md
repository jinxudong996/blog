



> `Blob` 对象表示一个不可变、原始数据的类文件对象。它的数据可以按文本或二进制的格式进行读取，也可以转换成 [`ReadableStream`](https://developer.mozilla.org/zh-CN/docs/Web/API/ReadableStream) 来用于数据操作。 
>
> Blob 表示的不一定是JavaScript原生格式的数据。[`File`](https://developer.mozilla.org/zh-CN/docs/Web/API/File) 接口基于`Blob`，继承了 blob 的功能并将其扩展使其支持用户系统上的文件。

Blob通常由一个可选的MIME类型的字符串type和 blobParts组成。

>  MIME（Multipurpose Internet Mail Extensions）多用途互联网邮件扩展类型，是设定某种扩展名的文件用一种应用程序来打开的方式类型，当该扩展名文件被访问的时候，浏览器会自动使用指定应用程序来打开。多用于指定一些客户端自定义的文件名，以及一些媒体文件打开方式。 常见的 MIME 类型有：超文本标记语言文本 .html text/html、PNG图像 .png image/png、普通文本 .txt text/plain 等。 

Blob构造函数的语法为

```javascript
let aBlob = new Blob(blobParts, options);
```

> - *array* 是一个由[`ArrayBuffer`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer), [`ArrayBufferView`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/TypedArray), [`Blob`](https://developer.mozilla.org/zh-CN/docs/Web/API/Blob), [`DOMString`](https://developer.mozilla.org/zh-CN/docs/Web/API/DOMString) 等对象构成的 [`Array`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array) ，或者其他类似对象的混合体，它将会被放进 [`Blob`](https://developer.mozilla.org/zh-CN/docs/Web/API/Blob)。DOMStrings会被编码为UTF-8。
>
> - options是一个可选的BlobPropertyBag字典，它可能会指定如下两个属性：
>
>      - `type`，默认值为 `""`，它代表了将会被放入到blob中的数组内容的MIME类型。
>  - `endings`，默认值为`"transparent"`，用于指定包含行结束符`\n`的字符串如何被写入。 它是以下两个值中的一个： `"native"`，代表行结束符会被更改为适合宿主操作系统文件系统的换行符，或者 `"transparent"`，代表会保持blob中保存的结束符不变

```javascript
const b = new Blob(['hello world'],{type:'text/plain'})
console.log(b)
Blob {size: 11, type: 'text/plain'}
    size: 11
    type: "text/plain"
    [[Prototype]]: Blob
```

Blob属性有两个：

1. size，只读，Blob对象中的所包含的数据大小。
2. type，只读，表明Blob对象总所包含数据的类型。

常用的方法有：

- slice([start[, end[, contentType]]])：返回一个新的 Blob 对象，包含了源 Blob 对象中指定范围内的数据。
- stream()：返回一个能读取 blob 内容的 `ReadableStream`。
- text()：返回一个 Promise 对象且包含 blob 所有内容的 UTF-8 格式的 `USVString`。
- arrayBuffer()：返回一个 Promise 对象且包含 blob 所有内容的二进制格式的 `ArrayBuffer`。



###### 使用场景

1.比较常用的就是用在文件下载上

以前可以使用表单下载

```javascript
export const downloadFileParams = (url, params = {}) => {
  const form = document.createElement('form')
  form.style.display = 'none'
  form.action = `${url}`
  form.method = 'post'
  // form.target = '_blank'

  Object.keys(params).forEach(item => {
    const input = document.createElement('input')
    input.type = 'hidden'
    input.name = item
    input.value = params[item]
    form.appendChild(input)
  })

  document.body.appendChild(form)
  form.submit()
  form.remove()
}
```

这种方式主要通过创建一个from表单进行前后端数据交互，后端返回数据流进行下载。

通过axios前后端交互，后端返回流下载

```javascript
Axios({
  method: 'post',
  url: url,
  data: params,
  responseType: 'blob', //此处是设置请求的为流文件,
}).then(res => {
  try{
    let fileName = res.headers['content-disposition'].split('=')[1];
    this.downLoadForm(res.data,fileName)
  }catch(e){
    var reader = new FileReader()
    var that = this;
    reader.addEventListener('loadend', function (e) {
      let errorMsg = '' //报错信息
      if(+"\v1"){ //ie
        errorMsg = JSON.parse(e.target.result)['jsonError'][0]['_exceptionMessage']
      }else{
        errorMsg = e.jsonError[0]._exceptionMessage
      }
      
      that.$message({
        message: errorMsg,
        type: "error",
      });
    })
    reader.readAsText(res.data)
  }
})
if(this.errorMsg){
  this.$message.error(this.errorMsg.toString().split(':')[1])
  return;
}
```

通过设置responseType

```javascript
downLoadForm(res, name) {
  const blob = new Blob([res]);
  if (window.navigator.msSaveOrOpenBlob) {
    // window.navigator.msSaveBlob(blob, name);
    window.navigator.msSaveOrOpenBlob(blob, name)
  } else {
    const link = document.createElement('a');
    link.style.display = 'none';
    link.href = window.URL.createObjectURL(blob);
   //  name=name.replaceAll("+",'%20').replaceAll("%2B",'+');
    link.setAttribute('download', decodeURI(name) );
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
},
```

上面两种主要的区别是前后盾交互的方式，前一种是传统的表单，后一种是ajax。表单前后端交互，更像是一种黑盒，下载数据前后无法操作，如果后端报错就会下载一个空页面，体验不是很好。通过a标签的downLoadFrom属性，利用try、catch如果下载出错，可以进行提示。downLoadForm方法中，使用URL.createObjectURL方法将Blob转化成了URL，利用download属性进行下载。接下来学习下URL接口。

2.用Blob用作URL。

>  **`URL`**接口用于解析，构造，规范化和编码 [URLs](https://developer.mozilla.org/zh-CN/docs/Glossary/URL)。 它通过提供允许您轻松阅读和修改URL组件的属性来工作。 通常，通过在调用URL的构造函数时将URL指定为字符串或提供相对URL和基本URL来创建新的URL对象。 然后，您可以轻松读取URL的已解析组成部分或对URL进行更改。 

 其中URL有一两个静态方法：

-  **`URL.createObjectURL()`** ： 静态方法会创建一个 [`DOMString`](https://developer.mozilla.org/zh-CN/docs/Web/API/DOMString)，其中包含一个表示参数中给出的对象的URL。这个 URL 的生命周期和创建它的窗口中的 [`document`](https://developer.mozilla.org/zh-CN/docs/Web/API/Document) 绑定。这个新的URL 对象表示指定的 [`File`](https://developer.mozilla.org/zh-CN/docs/Web/API/File) 对象或 [`Blob`](https://developer.mozilla.org/zh-CN/docs/Web/API/Blob) 对象。 
-  **`URL.revokeObjectURL()`** 静态方法用来释放一个之前已经存在的、通过调用 [`URL.createObjectURL()`](https://developer.mozilla.org/zh-CN/docs/Web/API/URL/createObjectURL) 创建的 URL 对象。当你结束使用某个 URL 对象之后，应该通过调用这个方法来让浏览器知道不用在内存中继续保留对这个文件的引用了 

实际上也可以将Blob转化为base64，可以使用FileRender构造函数。

> FileReader 对象允许Web应用程序异步读取存储在用户计算机上的文件（或原始数据缓冲区）的内容，使用 [`File`](https://developer.mozilla.org/zh-CN/docs/Web/API/File) 或 [`Blob`](https://developer.mozilla.org/zh-CN/docs/Web/API/Blob) 对象指定要读取的文件或数据。
>
> 其中File对象可以是来自用户在一个[`input`](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/Input)元素上选择文件后返回的[`FileList`](https://developer.mozilla.org/zh-CN/docs/Web/API/FileList)对象,也可以来自拖放操作生成的 [`DataTransfer`](https://developer.mozilla.org/zh-CN/docs/Web/API/DataTransfer)对象,还可以是来自在一个[`HTMLCanvasElement`](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLCanvasElement)上执行`mozGetAsFile()`方法后返回结果。
>
> 重要提示： FileReader仅用于以安全的方式从用户（远程）系统读取文件内容 它不能用于从文件系统中按路径名简单地读取文件。 要在JavaScript中按路径名读取文件，应使用标准Ajax解决方案进行服务器端文件读取，如果读取跨域，则使用CORS权限。

常用的方法有

- abort():中止读取操作。在返回时，`readyState`属性为`DONE`
- readAsArrayBuffer(): 开始读取指定的 [`Blob`](https://developer.mozilla.org/zh-CN/docs/Web/API/Blob)中的内容, 一旦完成, result 属性中保存的将是被读取文件的 [`ArrayBuffer`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer) 数据对象.
- readAsBinaryString():开始读取指定的[`Blob`](https://developer.mozilla.org/zh-CN/docs/Web/API/Blob)中的内容。一旦完成，`result`属性中将包含所读取文件的原始二进制数据。
- readAsText():开始读取指定的[`Blob`](https://developer.mozilla.org/zh-CN/docs/Web/API/Blob)中的内容。一旦完成，`result`属性中将包含一个字符串以表示所读取的文件内容。
- readAaDataURL():开始读取指定的[`Blob`](https://developer.mozilla.org/zh-CN/docs/Web/API/Blob)中的内容。一旦完成，`result`属性中将包含一个`data:` URL格式的Base64字符串以表示所读取文件的内容。

```javascript
getBase64(file) {
  return new Promise((resolve, reject) => {
    let reader = new FileReader();
    let fileResult = '';
    reader.readAsDataURL(file); //开始转
    reader.onload = function () {
      fileResult = reader.result;
    }; //转失败
    reader.onerror = function (error) {
      reject(error);
    }; //转结束  就 resolve 出去
    reader.onloadend = function () {
      resolve(fileResult);
    };
  });
},
```

而base64转化为Blob对象，

```javascript
function dataUrlToBlob(base64, mimeType) {
  let bytes = window.atob(base64.split(",")[1]);
  let ab = new ArrayBuffer(bytes.length);
  let ia = new Uint8Array(ab);
  for (let i = 0; i < bytes.length; i++) {
    ia[i] = bytes.charCodeAt(i);
  }
  return new Blob([ab], { type: mimeType });
}
```

如果要将Blob对象转化为File对象，有两种方式。

```javascript
baseToBlob(FileBase,id){
  let timestamp = Date.parse(new Date());
  let fileName = timestamp + '.png';
  let bstr = atob(FileBase)
  let n = bstr.length
  let u8arr = new Uint8Array(n)
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n)
  }
  return new File([u8arr], fileName, {
    type: 'image/png',
  })
},
```

然后File()构造函数IE不兼容，可以在Blob对象上添加两个属性即可。

```javascript
baseToBlob(FileBase,id){
  let timestamp = Date.parse(new Date());
  let fileName = timestamp + '.png';
  let bstr = atob(FileBase)
  let n = bstr.length
  let u8arr = new Uint8Array(n)
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n)
  }
  let blob = new Blob([u8arr]);
  return this.blobToFile(blob,fileName)
},
blobToFile(blob,fileName){
  Blob.lastModifieDate = new Date();
  Blob.name = fileName;
  return Blob;
}  
```



###### 图片压缩

在前端实现图片压缩，可以使用Canvas对象的toDataURL()方法，该方法接受type和encoderOptions两个可选参数：

- type表示图片格式，默认为image/png
- encoderOptions表示图片的质量，在指定图片格式为image/jpeg或image/webp，可以从0到1的区间选择图片的质量，超出范围默认为0.92。

```javascript
const MAX_WIDTH = 800; // 图片最大宽度

function compress(base64, quality, mimeType) {
  let canvas = document.createElement("canvas");
  let img = document.createElement("img");
  img.crossOrigin = "anonymous";
  return new Promise((resolve, reject) => {
    img.src = base64;
    img.onload = () => {
      let targetWidth, targetHeight;
      if (img.width > MAX_WIDTH) {
        targetWidth = MAX_WIDTH;
        targetHeight = (img.height * MAX_WIDTH) / img.width;
      } else {
        targetWidth = img.width;
        targetHeight = img.height;
      }
      canvas.width = targetWidth;
      canvas.height = targetHeight;
      let ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, targetWidth, targetHeight); // 清除画布
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      let imageData = canvas.toDataURL(mimeType, quality / 100);
      resolve(imageData);
    };
  });
}
```

完整的图片压缩的例子

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>本地图片压缩</title>
  </head>
  <body>
    <input type="file" accept="image/*" onchange="loadFile(event)" />
    <script src="./compress.js"></script>
    <script>
      const loadFile = function (event) {
        const reader = new FileReader();
        reader.onload = async function () {
          let compressedDataURL = await compress(
            reader.result,
            90,
            "image/jpeg"
          );
          let compressedImageBlob = dataUrlToBlob(compressedDataURL);
          uploadFile("https://httpbin.org/post", compressedImageBlob);
        };
        reader.readAsDataURL(event.target.files[0]);
      };
      function uploadFile(url, blob) {
        let formData = new FormData();
        let request = new XMLHttpRequest();
        formData.append("image", blob);
        request.open("POST", url, true);
        request.send(formData);
      }
      function dataUrlToBlob(base64, mimeType) {
        let bytes = window.atob(base64.split(",")[1]);
        let ab = new ArrayBuffer(bytes.length);
        let ia = new Uint8Array(ab);
        for (let i = 0; i < bytes.length; i++) {
          ia[i] = bytes.charCodeAt(i);
        }
        return new Blob([ab], { type: mimeType });
      }
        
      const MAX_WIDTH = 800; // 图片最大宽度

      function compress(base64, quality, mimeType) {
        let canvas = document.createElement("canvas");
        let img = document.createElement("img");
        img.crossOrigin = "anonymous";
        return new Promise((resolve, reject) => {
          img.src = base64;
          img.onload = () => {
            let targetWidth, targetHeight;
            if (img.width > MAX_WIDTH) {
              targetWidth = MAX_WIDTH;
              targetHeight = (img.height * MAX_WIDTH) / img.width;
            } else {
              targetWidth = img.width;
              targetHeight = img.height;
            }
            canvas.width = targetWidth;
            canvas.height = targetHeight;
            let ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, targetWidth, targetHeight); // 清除画布
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            let imageData = canvas.toDataURL(mimeType, quality / 100);
            resolve(imageData);
          };
        });
      }
    </script>
  </body>
</html>
```