随着ai日新月异的发展，ai编程助手越来越多，功能也越来越强大，先介绍下目前市面上比较流行的AI编程助手

1. GitHub Copilot ++

    基于OpenAI的GPT模型，能理解上下文并生成高质量代码 ，支持VS Code，价格较贵

2. OpenAAI Codex2025 

    可同时处理多个编程任务，如代码重构、测试生成 ，但单次任务时间有限，无法处理超长文件

3. 通义灵码

   这个唯一的优点就是免费，它的路还长

4. cursor

   可以基于整个代码库提问，给出精准建议，也支持复杂的任务管理。

相比之下cursor当前仍然属于第一梯队，能够极大的解放生产力，接下来这篇文章按照环境、基础、进阶和实战四个部分来详细的学习下这个工具。

##### 基础篇

###### 安装

1. 访问 Cursor 官网：[www.cursor.com/](https://www.cursor.com/ "https://www.cursor.com/")
2. 点击 "Download" 按钮下载安装包，Cursor 会根据您的操作系统自动选择合适的安装包，安装流程也很简单，一路next即可。
3. 可以使用GitHub账号来注册账号，然后倒入本地的VS Code配置、插件，界面也和VS Code基本类似，对于前端开发人员非常友好

###### 模式

cursor有三种开发模式，分别是`Ask模式`、`Agent模式`和`Manual模式`

1. Ask是最基础的对话模式，可以直接向AI提问，来获得代码相关的帮助和建议，适合一些简单的代码问题咨询，当需要快速获取答案时可以使用这个模式。
2. Agent是最强大的模式，可以主动搜索代码仓库，读取和编辑文件，执行复杂的多步骤任务，适合新功能开发和调试问题
3. Manual模式，最基础的模式，AI只能提供建议，不能直接执行操作。

举个小例子，切换模式未Agent。输入到` 帮我写一个工具方法，对象深拷贝 `

```ts
/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-06-16 11:27:41
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-06-16 11:28:33
 * @FilePath: \cursor\001.ts
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
/**
 * 深拷贝工具方法
 * @param source 需要拷贝的源数据
 * @returns 拷贝后的新数据
 */
export function deepClone<T>(source: T): T {
  // 处理 null 和 undefined
  if (source == null) {
    return source;
  }

  // 处理日期对象
  if (source instanceof Date) {
    return new Date(source.getTime()) as any;
  }

  // 处理正则表达式
  if (source instanceof RegExp) {
    return new RegExp(source.source, source.flags) as any;
  }

  // 处理数组
  if (Array.isArray(source)) {
    return source.map((item) => deepClone(item)) as any;
  }

  // 处理对象
  if (typeof source === "object") {
    const target = {} as any;
    for (const key in source) {
      if (Object.prototype.hasOwnProperty.call(source, key)) {
        target[key] = deepClone(source[key]);
      }
    }
    return target;
  }

  // 处理基本类型
  return source;
}

// 使用示例
const example = {
  name: "test",
  age: 25,
  date: new Date(),
  arr: [1, 2, { a: 1 }],
  obj: {
    foo: "bar",
    nested: {
      value: 123,
    },
  },
};

const cloned = deepClone(example);
console.log(cloned);

```

方法考虑的很周到，还时非常不错的

当然也可以唤醒一个内联聊天窗口，比如生成新代码、修改现有代码，通过快捷键`ctrl k`来唤醒。



###### 代码库索引

代码库索引是 Cursor 最强大的功能之一。它通过为代码文件创建嵌入向量（Embeddings），帮助 AI 全面理解你的项目。这个功能让 AI 能够"看见"整个代码库，而不仅仅是当前打开的文件

##### 





##### 进阶篇





##### 实战篇

Chromo





