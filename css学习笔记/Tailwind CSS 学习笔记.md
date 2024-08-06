

##### 安装

首先执行命令安装

` npm install -D tailwindcss postcss autoprefixer `

然后再根目录下创建一个 `postcss.config.js`  

```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

 接下来，你需要在项目中创建一个Tailwind CSS配置文件 ，

` npx tailwindcss init `，会在根目录下生成一个`tailwind.config.js`，

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

 配置文件可以帮助你自定义和扩展Tailwind CSS的样式和功能 

其中：

> - `content`字段用于指定Tailwind CSS应该用于处理哪些文件。在这个配置中，`content: []`表示没有指定任何文件，这意味着Tailwind CSS将不会应用于任何文件。如果你想让Tailwind CSS应用于特定的文件或目录，你可以在这里指定它们。
> - `theme`字段允许你扩展或覆盖Tailwind CSS的默认主题配置。在这个配置中，`theme: { extend: {} }`表示没有对主题进行任何扩或覆盖。你可以在`extend`字段中添加自定义的主题配置，例如添加新的颜色、字体、间距等。
> -  `plugins`字段用于添加额外的插件来扩展Tailwind CSS的功能。在这个配置中，`plugins: []`表示没有添加任何插件。 

然后在`src/assets/tailwindcss.css`目录下生成`tailwindcss.css`文件，在该文件中使用`@tailwind`指令来引入Tailwind的样式 ：

```js
@tailwind base;
@tailwind components;
@tailwind utilities;
```

在`main.js`中引入该文件即可。`import './assets/tailwindcss.css`

这里就可以在项目中使用了。

比如：

```vue
<div class="bg-blue-500 p-4">
	<p class="text-white">Hello, Tailwind CSS!</p>
</div>
```

就可以看到样式已经生效了。



##### 基础

###### 高度

比如

```
<div class="w-40 h-40 bg-red-500">width and height</div>
```

这里w-40和h-40，就是10rem，换算成px就是160px，bg-red-500就是背景色设置为红色，这里如果想用16进制的话，可以这么做：

在`tailwind.config.js`中定义主题：

```js
theme: {
    extend: {
      colors: {
        'custom-red': '#FF5733', // 自定义的红色
      },
    },
  },
```

然后直接使用即可：

```vue
<div class="w-40 h-40 bg-custom-red">width and height</div>
```

这里的w-40是10rem，换算成px就是160px，及1rem就是16px，这是因为浏览器默认的html的font-size就是16px，如果要定制化的话，可以这么做：

比我我想让1rem = 10px，同时一个单元就是1rem，即w-40 = 40rem，

首先在`src/assets/tailwindcss.css`加上样式：

```css
html {

  font-size: 10px;

}
```

然后在`tailwind.config.js`中定义下间距：

```js
extend: {
      spacing: {
        '1': '1rem', // 10px
        '2': '2rem', // 20px
        '40':'40rem',
        // ... 更多自定义间距
      },
      colors: {
        'custom-red': '#FF5733', // 自定义的红色
      },
    },
```

这样w-40 换算过来的单位就是40rem 也就是400px

同时也可以通过` w-[] `来指定，比如：

```html
<div class="w-[20rem] h-40 bg-custom-red">width and height</div>
```

也可以通过`w-1/4`来指定百分比

```html
<div class="w-1/4 h-40 bg-custom-red">width and height</div>
```







###### 边距

```html
<div class="mt-20 w-1/4 h-40 bg-custom-red">width and height</div>
```

这个也比较简单，简写就是第一个字母和第二个字母的缩写，

还有一个比较常见的居中写法： `margin: 0 auto` 

```html
<div class="w-1/4 h-40 mx-auto bg-custom-red">width and height</div>
```

###### 边框

设置一个div的边框为：` border:2px solid red ;`，用 tailwindcss  可以这么写：

```html
<div class="border-2 w-20 h-20 border-solid border-custom-red"></div>
```

像设置边框的弧度，有这样几个内置类名

rounded 👉 `border-radius: 0.25rem; /* 4px */`

rounded-md 👉 `border-radius: 0.375rem; /* 6px */`

rounded-lg 👉 `border-radius: 0.5rem; /* 8px */`

rounded-full 👉 `border-start-start-radius: 9999px; border-end-start-radius: 9999px;`

如果想自定义设置的话，首先在 `tailwind.config.js` 文件中，需要定义自定义的圆角半径 

```
theme: {
    extend: {
      spacing: {
        '1': '1rem', // 10px
        '2': '2rem', // 20px
        '40':'40rem',
        // ... 更多自定义间距
      },
      colors: {
        'custom-red': '#FF5733', // 自定义的红色
      },
      borderRadius: {
        '0.3': '0.3rem',
      },
    },
```



```vue
<div class="border-2 w-20 h-20 border-solid border-custom-red rounded-0.3"></div>
```

就相当于设置这个div的`border-radius:0.3rem`



###### 文本

设置字体大小，可以通过` text-[] `来自定义，比如：

```html
<div class="text-[1.8rem]">设置字体大小</div>
```

当然也有一些内置类，比如` text-sm `、` text-base `等，不如` text-[] `好使。

文本对齐的话，也比较简单啦，看名字就知道啥意思了，

` text-left `，` text-center `和` text-right `

设置`font-weight`，这个比较难记，用的时候问下GPT或者查询下文档即可。



###### 颜色

设置字体颜色，

```vue
<div class="text-[1.8rem] font-extrabold text-custom-red">设置字体大小</div>
```

设置背景色

```vue
<div class="text-[1.8rem] font-extrabold text-custom-red bg-orange-500">设置字体大小</div>
```



































