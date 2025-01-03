##### 介绍

LangChain 是一款围绕 LLMs 构建的开发框架，一边对接各类 LLM 模型，我们可以快速切换使用的模型；另一边提供了一系列工具、组件和接口，可以快速集成外部系统，极大简化了开发 LLM 应用的流程。

对于 LLM 应用开发学习，LangChain 是个不错的选择，框架对 LLM 开发进行了很好的划分，我们按着这些模块学习，就能掌握 LLM 应用开发的各个环节。

###### 安装

新建一个node项目，运行`npm init -y`，在`package.json`中添加`"type": "module",`使用ES模块来运行该项目。然后依次安装`@langchain/core`，`@langchain/openai`，`dotenv`。由于申请GPT的key很是麻烦，使用的第三方供应商。在项目根目录下新建`.env`，

```
OPENAI_API_KEY=your key
```

新建文件`app.js`

```js
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "@langchain/core/messages";
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
  }
});

(async () => {
  try {
    const response = await model.invoke([
      new HumanMessage("帮我写一首以向日葵为主题关于爱情的七律诗")
    ]);
    console.log(response.content);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();
//输出结果
。。。
花心向阳芬芳溢，爱意绵绵随风扬。
。。。
```

上面的是对话模型，接下来看一个llm的简单例子

```js
import { OpenAI } from "@langchain/openai";
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const model = new OpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
  },
});

(async () => {
  try {
    const prompt = "帮我写一首以向日葵为主题关于爱情的七律诗";
    const response = await model.invoke(prompt);
    console.log(response);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();
```

我们的环境搭建的没问题了，接下来进一步学习该框架。

##### prompt

 Prompt 是大模型的核心，传统方式我们一般使用字符串拼接或者模版字符串来构造 prompt，而有了 langchain 后，我们可以构建可复用的 prompt 来让我们更工程化的管理和构建 prompt，从而制作更复杂的 chat bot 

###### 字符串模板PromptTemplate

在python中，有`PromptTemplate`这样一个方法可以实现模板字符串，比如

```python
#字符模板
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template("你是一个{name},帮我起1个具有{county}特色的{sex}名字")
prompt.format(name="算命大师",county="法国",sex="女孩")
```

在js中我们可以使用占位符轻松的实现这个功能

```js
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "@langchain/core/messages";
import { PromptTemplate } from "@langchain/core/prompts"
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
  }
});
// 定义模板字符串
const template = "你是一个{name},帮我起1个具有{county}特色的{sex}名字";

// 创建 PromptTemplate 实例
const promptTemplate = new PromptTemplate({
  template: template,
  inputVariables: ["name", "county", "sex"],
});

(async () => {
  try {
    const variables = {
      name: "算命大师",
      county: "法国",
      sex: "女孩"
    };
    const formattedPrompt = await promptTemplate.format(variables);
    console.log(formattedPrompt)
    const response = await model.invoke([
      new HumanMessage(formattedPrompt)
    ]);
    console.log(response.content);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();
你是一个算命大师,帮我起1个具有法国特色的女孩名字
当然，我建议起一个具有法国特色的女孩名字叫做菲奥娜（Fiona）。这个名字在法国很常
见，意为“白皙的，纯净的”。希望你喜欢这个取名建议！
```

这个`PromptTemplate.format`实际上也可以通过js的字符串模板来替换：

```js
// 定义模板字符串
const template = "你是一个{name},帮我起1个具有{county}特色的{sex}名字";

// 替换占位符
function formatPrompt(template, variables) {
  return template.replace(/{([^}]+)}/g, (match, key) => variables[key] || match);
}

const formattedPrompt = formatPrompt(template, variables);
```

这里定义了`formatPrompt`方法，这个方法就是来匹配模板中的{}，然后用这个json中的value去替换，就实现了一个字符串模板的功能。把动态的部分给提取出来，后续可以根据`variables`的内容，来动态的确定模板的内容，非常的灵活。

###### 对话模板ChatPromptTemplate

```js
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";
import { ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate } from "@langchain/core/prompts";
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
    apiKey: process.env.OPENAI_API_KEY, // 确保 API 密钥已设置
  }
});

// 定义 ChatPromptTemplate
const chatPrompt = ChatPromptTemplate.fromMessages([
  ["system", "你是一个老师. 你的名字叫{name}."],
  ["human", "你好{name},天王盖地虎，下面一句是啥？"],
  ["ai", "你好！宝塔镇河妖!"],
  ["human", "你叫什么名字呢?"],
  ["ai", "你好！我叫{name}"],
  ["human", "{user_input}"],
]);

(async () => {
  try {
    const variables = {
      name: "teacher王",
      user_input: "你是谁啊?"
    };

    // 格式化提示
    const formattedChatPrompt = await chatPrompt.formatMessages(variables);
    // 调用模型
    const response = await model.invoke(formattedChatPrompt);
    console.log(response.content);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();
//輸出
我是一个智能助手，可以回答你的问题和提供信息。我叫teacher王。有什么可以帮助你的吗？
```

换种方式也可以

```js
const sy = new SystemMessage({
  content: "你是一个起名大师",
  additional_kwargs: { 大师姓名: "陈瞎子" }
});

const hu = new HumanMessage({
  content: "请问大师叫什么?"
});

const ai = new AIMessage({
  content: "我叫陈瞎子"
});

// 定义 ChatPromptTemplate
const chatPrompt = ChatPromptTemplate.fromMessages([
  sy,
  hu,
  ai
]);
//输出
起名大师虽是我的称号，实则只是我在这个领域中的敬称，希望能为
你提供满意的取名帮助。有什么名字需要我帮忙起吗？
```



###### 自定义模板

当上述模板不满足要求时，也可以使用自定义模板，js在操作字符串方面还是非常灵活的。

接下来做一个解释代码的机器人

```js
import { ChatOpenAI } from "@langchain/openai";
import { SystemMessagePromptTemplate, ChatPromptTemplate, PromptTemplate } from "@langchain/core/prompts";
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

// 定义一个简单的函数作为示例效果
function helloWorld(abc) {
  console.log("Hello, world!");
  return abc;
}

// 定义提示词模板
const PROMPT = `你是一个非常有经验和天赋的程序员，现在给你如下函数名称，你会按照如下格式，输出这段代码的名称、源代码、中文解释。
函数名称: {function_name}
源代码:
{source_code}
代码解释:
`;

function getFunctionSourceCode(func) {
  // 获取函数的源代码
  let sourceCode = func.toString();

  // 转义函数体内的大括号
  sourceCode = sourceCode.replace(/\{/g, '{{').replace(/\}/g, '}}');

  return sourceCode;
}
// 创建 PromptTemplate 实例
const promptTemplate = new PromptTemplate({
  template: PROMPT,
  inputVariables: ["function_name", "source_code"],
});

// 创建 ChatOpenAI 实例
const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
    apiKey: process.env.OPENAI_API_KEY, // 确保 API 密钥已设置
  }
});

(async () => {
  try {
    // 获得源代码
    const sourceCode = getFunctionSourceCode(helloWorld);

    // 格式化提示
    const formattedPrompt = await promptTemplate.format({
      function_name: helloWorld.name,
      source_code: sourceCode,
    });
    console.log(formattedPrompt);
    // 创建 SystemMessagePromptTemplate 实例
    const systemMessagePrompt = SystemMessagePromptTemplate.fromTemplate(formattedPrompt);

    // 定义 ChatPromptTemplate
    const chatPrompt = ChatPromptTemplate.fromMessages([
      systemMessagePrompt
    ]);

    // 格式化聊天提示
    const formattedChatPrompt = await chatPrompt.formatMessages({});
    console.log(formattedChatPrompt);

    // 调用模型
    const response = await model.invoke(formattedChatPrompt);
    console.log(response.content);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();
//输出
代码解释:
该函数名为helloWorld，接收一个参数abc，并在控制台打印"Hello, world!"，然后返回参数abc
```

这里实际上也就是前面的字符串模板，用这个这个字符串模板定义一个系统对话，然后再将`formattedChatPrompt`喂给模型。这里有个坑啊，刚开始helloWorld方法直接传入字符串，一直报错[无效输入](https://js.langchain.com/docs/troubleshooting/errors/INVALID_PROMPT_INPUT/)，后来在官网提示下改正了。

###### 序列化

使用文件来管理我们的提示词模板。

```js
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "@langchain/core/messages";
import { PromptTemplate } from "@langchain/core/prompts";
import * as dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';


// 加载环境变量
dotenv.config();

const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
  }
});

// 定义模板字符串
const templateContent = fs.readFileSync('./template.txt', 'utf-8');
console.log(templateContent);

// 创建 PromptTemplate 实例
const promptTemplate = new PromptTemplate({
  template: templateContent,
  inputVariables: ["name", "county", "sex"],
});

(async () => {
  try {
    const variables = {
      name: "算命大师",
      county: "中国",
      sex: "女孩"
    };

    // const formattedPrompt = formatPrompt(template, variables);
    const formattedPrompt = await promptTemplate.format(variables);
    console.log(formattedPrompt);

    const response = await model.invoke([
      new HumanMessage(formattedPrompt)
    ]);
    console.log(response.content);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();
```

这里借助了node的fs模块来读取文件，然后通过promptTemplate将文件的内容生成模板。

###### 示例选择器

现在ChatGPT-4 Turbo可以输出128K长度的字符，这个长度相当于一本三百页的书籍了，在实际应用中是没有这么大的窗口来展示的，这里就需要对输出做一个限制。常见的有以下三种限制方式：

1. 根据长度要求智能选择示例

   这里官网例子有点问题，折磨了好久搞不明白。

   ```js
   import { ChatOpenAI } from "@langchain/openai";
   import { HumanMessage } from "@langchain/core/messages";
   import { PromptTemplate,FewShotPromptTemplate } from "@langchain/core/prompts";
   import {LengthBasedExampleSelector} from "@langchain/core/example_selectors";
   import * as dotenv from 'dotenv';
   
   // 加载环境变量
   dotenv.config();
   
   const examples = [
     { input: "happy", output: "sad" },
     { input: "tall", output: "short" },
     { input: "energetic", output: "lethargic" },
     { input: "sunny", output: "gloomy" },
     { input: "windy", output: "calm" },
   ]
   
   const model = new ChatOpenAI({
     configuration: {
       baseURL: "https://ai-yyds.com/v1",
       apiKey: process.env.OPENAI_API_KEY, // 确保 API 密钥已设置
     }
   });
   const exampleSelector = new LengthBasedExampleSelector(
     [ 
       { input: "happy", output: "sad" },
       { input: "tall", output: "short" },
       { input: "energetic", output: "lethargic" },
       { input: "sunny", output: "gloomy" },
       { input: "windy", output: "calm" },
     ],
     {
       examplePrompt: new PromptTemplate({
         inputVariables: ["input", "output"],
         template: "Input: {input}\nOutput: {output}",
       }),
       maxLength: 100,
   });
   const dynamicPrompt = new FewShotPromptTemplate({
     exampleSelector:exampleSelector,
     examplePrompt: new PromptTemplate({
       inputVariables: ["input", "output"],
       template: "Input: {input}\nOutput: {output}",
     }),
     prefix: "Give the antonym of every input",
     suffix: "Input: {adjective}\nOutput:",
     inputVariables: ["adjective"],
   });
   
   // console.log(dynamicPrompt.format({ adjective: "big" }));
   const longString = "big and huge adn massive and large and gigantic and tall and much much much much much much bigger then everyone";
   (async () => {
     try {
       const selectedExamples = await exampleSelector.selectExamples({ adjective: 123 });
       console.log("Selected Examples:", selectedExamples);
       const formattedPrompt = await dynamicPrompt.format({ adjective: longString });
       console.log(123)
       console.log(formattedPrompt);
   
       const response = await model.invoke([
         formattedPrompt
       ]);
       console.log(response.content);
     } catch (error) {
       console.error("Error invoking the model:", error);
     }
   })();
   ```

   去python那边跑了下官网的示例没问题的，但是这个为啥跑不通，去提了个isuue，等回复吧，感觉是官网文档的问题。

2. 根据输入相似度选择示例(最大边际相关性)

   \- MMR是一种在信息检索中常用的方法，它的目标是在相关性和多样性之间找到一个平衡

   \- MMR会首先找出与输入最相似（即余弦相似度最大）的样本

   \- 然后在迭代添加样本的过程中，对于与已选择样本过于接近（即相似度过高）的样本进行惩罚

   \- MMR既能确保选出的样本与输入高度相关，又能保证选出的样本之间有足够的多样性

   \- 关注如何在相关性和多样性之间找到一个平衡

3. 根据输入相似度选择示例（最大余弦相似度）



###### 流失输出

```js
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "@langchain/core/messages";
// import { HumanMessage } from "@langchain/core/messages";
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
  },
  streaming: true, // 启用流式输出
});

(async () => {
  try {
    const response = await model.invoke([
      new HumanMessage("帮我写一首以向日葵为主题关于爱情的七律诗")
    ], {
      callbacks: [
        {
          handleLLMNewToken(token) {
            process.stdout.write(token); // 流式输出每个 token
          }
        }
      ]
    });
    console.log(); // 换行
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();
```



###### 统计token数量

```js
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "@langchain/core/messages";
// import { HumanMessage } from "@langchain/core/messages";
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
  },
  streaming: true, // 启用流式输出
  maxTokens:520,
});

(async () => {
  try {
    const response = await model.invoke([
      new HumanMessage("帮我写一首以向日葵为主题关于爱情的七律诗")
    ], {
      callbacks: [
        {
          handleLLMNewToken(token) {
            process.stdout.write(token); // 流式输出每个 token
          },
          handleLLMEnd(output) {
            console.log(); // 换行
            console.log("流式输出已完成");
            console.log("Token 使用情况:", output.llmOutput);
          }
        }
      ]
    });
    console.log(); // 换行
    console.log("流式输出已完成");
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();
```



##### RAG检索增强

大模型的缺点在与数据不够新，数据库的知识不是最新的，而且对于相关领域的知识是有欠缺的。通过RAG让我们的大模型更加聪明。小册[从前端到AI](https://juejin.cn/book/7347579913702293567/section/7351410645298135091)J对于ARG的原理讲的非常好，很通俗，这里贴一下：

RAG 的基本流程就是：

1. 用户输入提问
2. 检索：根据用户提问对 向量数据库 进行相似性检测，查找与回答用户问题最相关的内容
3. 增强：根据检索的结果，生成 prompt。 一般都会涉及 “仅依赖下述信息源来回答问题” 这种限制 llm 参考信息源的语句，来减少幻想，让回答更加聚焦
4. 生成：将增强后的 prompt 传递给 llm，返回数据给用户

 RAG 就是哪里有问题解决哪里，既然大模型无法获得最新和内部的数据集，那我们就使用外挂的向量数据库为 llm 提供最新和内部的数据库。既然大模型有幻想问题，我们就将回答问题所需要的信息和知识编码到上下文中，强制大模型只参考这些内容进行回答。 

**1. 加载数据**
因为想要根据用户的提问进行语意检索，我们需要将数据集放到向量数据库中，所以我们需要将不同的数据源加载进来。这里就涉及到多种数据源，例如 pdf、code、现存数据库、云数据库等等。

这里 langchain 提供非常丰富的集成工具，帮助我们加载来自多个数据源的数据。这个详细的内容会在对应章节介绍场景的数据源的加载方式。

**2. 切分数据**
gpt3.5t 的上下文窗口是 16k，gpt4t 上下文窗口是 128k，而我们很多数据源都很容易比这个大。更何况，用户的提问经常涉及多个数据源，所以我们需要对数据集进行语意化的切分，根据内容的特点和目标大模型的特点、上下文窗口等，对数据源进行合适的切分。

这里听起来比较容易，但考虑到数据源的多种多样和自然语言的特点，事实上切分函数的选择和参数的设定是非常难以控制的。理论上我们是希望每个文档块都是语意相关，并且相互独立的。

**3. 嵌入（embedding）**
这部分对没有机器学习相关背景的同学不容易理解。这里我们用最简单的词袋（words bag）模型来描述一下最简单的 embedding 过程，让大家更具象化的理解这个。

a. 词袋模型就是最简化的情况，把一篇 句子/文章 中的单词提前出来，就像放到一个袋子里一样，认为单词之间是独立的，并不关心词与词之间的上下文关系。
b. 假设我们有十篇英语文章，那我们可以把每个文章拆分成单词，并且还原成最初的形势（例如 did、does => do），然后我们统计每个词出现的次数。 我们简化一下假设最后结果就是

```makefile
makefile复制代码第一篇文章: 
apple: 10, phone:12

第二篇文章:
apple: 8, android: 10, phone: 18

第三篇文章:
banana: 6, juice: 10
```

c. 那我们尝试构建一个向量，也就是一个数组，每个位置有一个值，代表每个单词在这个文章中出现的次数

```csharp
csharp复制代码变量
[apple, banana, phone, android, juice]
```

那每篇文章，都能用一个变量来表示

```ini
ini复制代码第一篇文章: [10, 0, 12, 0, 0]
第二篇文章: [8, 0, 18, 10, 0]
第三篇文章: [0, 6, 0, 0, 10]
```

d. 这样我们就能把一篇文章用一个向量来表示了，然后我们可以用最简单的余弦定理去计算两个向量之间的夹角，以此确定两个向量的距离。 e. 这样，我们就有了通过向量和向量之间的余弦夹角的，来衡量文章之间相似度的能力，是不是很简单。

当然，这是最最最简单的 embedding 原理，不过是所有的 embedding 和相似性搜索都是类似的原理。

回到我们 RAG 流程中，我们将切分后的每一个文档块使用 embedding 算法转换成一个向量，存储到向量数据库中（vector store）中。这样，每一个原始数据都有一个对应的向量，可以用来检索。

**4.检索数据**
当所有需要的数据都存储到向量数据库中后，我们就可以把用户的提问也 embedding 成向量，用这个向量去向量数据库中进行检索，找到相似性最高的几个文档块，返回。

在这里，使用什么算法去计算向量之间的距离也是需要选择的，这个我们会在对应的章节进行介绍。

**5.增强 prompt**

在有了跟用户提问最相关的文档块后，我们根据文档块去构建 prompt。 

**6.生成**
然后就是将组装好的 prompt 传递给 chatbot 进行生成回答。





###### loader

loader让大模型具备实时学习的能力。

支持很多种数据格式的加载。

首先加载json文件

```json
import { JSONLoader } from "langchain/document_loaders/fs/json";

const loader = new JSONLoader("example.json");
const docs = await loader.load();
console.log("Loaded documents:", docs);
//输出
Loaded documents: [
  Document {
    pageContent: 'This is a sentence.',
    metadata: { source: 'example.json', line: 1 }
  },
  Document {
    pageContent: 'This is another sentence.',    
    metadata: { source: 'example.json', line: 2 }
  }
]
```

当然还支持常见的csv、doc和目录等，可以看下[文档](https://js.langchain.com/docs/integrations/document_loaders/file_loaders/)

###### 文档切割

文档拆分通常是许多应用程序的关键预处理步骤。它涉及将大文本分解成较小的、可管理的块。此过程提供了多种好处，例如确保对不同长度的文档进行一致处理、克服模型的输入大小限制以及提高检索系统中使用的文本表示的质量。有几种拆分文档的策略，每种策略都有各自的优势。 

接下来做一个文档切割的例子，文档切割主要有以下三个方面来考量的

1. 将文档分成小的、有意义的块(句子).

2. 将小的块组合成为一个更大的块，直到达到一定的大小.

3. 一旦达到一定的大小，接着开始创建与下一个块重叠的部分.

[官网](https://js.langchain.com/v0.2/docs/how_to/#text-splitters)上介绍了四种切割方法，分别是基于长度、文本结构、文档结构和语义的方式。

比如基于长度切割

```js
import { CharacterTextSplitter } from "@langchain/textsplitters";
const textSplitter = new CharacterTextSplitter({
  chunkSize: 100,
  chunkOverlap: 0,
});
const texts = await textSplitter.splitText(document);
```



接下来做一个文档总结翻译精炼的例子。lorder.txt是准备的一个很长的英文文档。

```js
import { ChatOpenAI } from "@langchain/openai";
import {
  SystemMessage,
  HumanMessage,
  AIMessage,
} from "@langchain/core/messages";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { CharacterTextSplitter } from "@langchain/textsplitters";
import fs from "fs";


const OPENAI_API_KEY = process.env.OPEN_API_KEY;
const OPENAI_API_BASE = process.env.OPENAI_API_BASE;
const OPENAI_MODEL = "gpt-3.5-turbo-16k";
const OPENAI_TOKEN_LIMIT = 8000;

// 加载文档
const content = fs.readFileSync("letter.txt", "utf-8");

// 使用 CharacterTextSplitter 分割文本
const textSplitter = new CharacterTextSplitter({
  chunkSize: 100,
  chunkOverlap: 0,
});

// 创建 ChatOpenAI 模型实例
const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
    apiKey: "sk-uK6mnTkdB4TT6EAODf1a24Da7a43456793B1C12a61D4D167", // 确保 API 密钥已设置
  },
});

(async () => {
  try {
    // 格式化聊天提示
    const texts = await textSplitter.splitText(content);
    // 创建聊天提示模板
    const chatPromptTemplate = ChatPromptTemplate.fromMessages([
      new SystemMessage("You are a helpful assistant."),
      new HumanMessage(`Here is the document content: ${texts.join("\n")}`),
      new AIMessage("Please summarize the document."),
    ]);
    const formattedChatPrompt = await chatPromptTemplate.formatMessages();

    // 调用模型进行总结
    const summaryResponse = await model.invoke(formattedChatPrompt);
    console.log("Summary:", summaryResponse.content);

    // 创建聊天提示模板进行翻译
    const translationPromptTemplate = ChatPromptTemplate.fromMessages([
      new SystemMessage("You are a helpful assistant."),
      new HumanMessage(`Here is the document content: ${texts.join("\n")}`),
      new AIMessage("Please translate the document to Chinese."),
    ]);

    // 格式化聊天提示
    const formattedTranslationPrompt =
      await translationPromptTemplate.formatMessages();

    // 调用模型进行翻译
    const translationResponse = await model.invoke(formattedTranslationPrompt);
    console.log("Translation:", translationResponse.content);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();

```

先用fs模块来加载本地的`letter.txt`，然后用`CharacterTextSplitter`来指定切割规则

其中：

- **`chunkSize: 100`**: 这个参数指定了每个文本块的最大字符数。在这个例子中，每个文本块最多包含 100 个字符。
- **`chunkOverlap: 0`**: 这个参数指定了相邻文本块之间的重叠字符数。在这个例子中，相邻的文本块之间没有重叠字符。

然后调用`textSplitter.splitText(content)`完成对文本的切割，将数据通过制定的角色来把数据喂给模型。



###### 文本向量化

文本向量化能够将文本转换为向量表示，便于在向量空间中进行快速查找和相似性度量。这种转换有助于提升文本处理的效率和准确性，特别是在语义搜索、问答系统等NLP任务中，能够显著提高应用的效果和性能。 

来简单的看下文本向量化的示例：

```js
import { TextLoader } from "langchain/document_loaders/fs/text";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { OpenAIEmbeddings } from "@langchain/openai";
import * as dotenv from "dotenv";

const loader = new TextLoader("kong.txt");

dotenv.config();
async function main() {
  const docs = await loader.load();

  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 100,
    chunkOverlap: 20,
  });

  const splitDocs = await splitter.splitDocuments(docs);
  // console.log(splitDocs);

  const embeddings = new OpenAIEmbeddings({
    configuration: {
      baseURL: "https://ai-yyds.com/v1",
    },
  });

  const res = await embeddings.embedQuery(splitDocs[0].pageContent);
  console.log(res);
}
main();
//输出
[
     0.017484097,   0.0005194439,    0.01524044,   -0.02138313,   -0.006707025,
    -0.010075929,   -0.022491278, -0.0058211917,  -0.007367125,   -0.030234626,]
```

 对数据生成 embedding 需要一定的花费，所以我们希望把 embedding 的结果持久化，这样可以在应用中持续复用。   [faiss](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Ffacebookresearch%2Ffaiss) 向量数据库是由 facebook 开源的数据库， 向量数据库中非常流行的开源解决方案。 

 在开发时，我们既可以用 js 进行 embedding 和持久化存储，并后续使用 js 读取已经持久化的向量数据库进行使用。也可以使用 python 进行 embedding 并持久化存储成文件，然后使用 js 进行读取和使用。如果未来对可靠性需求变大，也可以非常容易地将其数据库内容导出到其他数据库或者云数据库。这给我们足够的灵活性。 

```js
import { FaissStore } from "@langchain/community/vectorstores/faiss";
import { OpenAIEmbeddings } from "@langchain/openai";
import "faiss-node";

import * as dotenv from "dotenv";

dotenv.config();

const directory = "./kongyiji";
const embeddings = new OpenAIEmbeddings({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
  },
});

async function run() {
  const vectorstore = await FaissStore.load(directory, embeddings);

  const retriever = vectorstore.asRetriever(2);
  const res = await retriever.invoke("茴香豆是做什么用的");

  console.log(res);
}

run();
//
[
  {
    pageContent: '有喝酒的人便都看着他笑，有的叫道，“孔乙己，你脸上又添上新伤疤了！”他不回答，对柜里说，“温两碗酒，要一碟茴香豆。”便排
出九文大钱。他们又故意的高声嚷道，“你一定又偷了人家的东西了！”孔乙己睁大眼睛说',
    metadata: { source: '../data/kong.txt', loc: [Object] }
  },
  {
    pageContent: '有几回，邻居孩子听得笑声，也赶热闹，围住了孔乙己。他便给他们一人一颗。孩子吃完豆，仍然不散，眼睛都望着碟子。孔乙己着
了慌，伸开五指将碟子罩住，弯腰下去说道，“不多了，我已经不多了。”直起身又看一看豆',
    metadata: { source: '../data/kong.txt', loc: [Object] }
  }
]
```

可以看到输出结果并不是准确的结果，因为在提取的时候，是根据相似度进行度量的，所以如果用户提问的特别简洁，并没有相应的关键词，就会出现提取的信息错误的问题 。 如果用户提问的关键词缺少，或者恰好跟原文中的关键词不一致，就容易导致 retriever 返回的文档质量不高，影响最终 llm 的输出效果。 

接下来就要对其进一步优化，常见的思路有

 **`MultiQueryRetriever`**  

使用 LLM 去将用户的输入改写成多个不同写法，从不同的角度来表达同一个意思，来克服因为关键词或者细微措词导致检索效果差的问题。 

```js
import { FaissStore } from "@langchain/community/vectorstores/faiss";
import { OpenAIEmbeddings, ChatOpenAI } from "@langchain/openai";
import { MultiQueryRetriever } from "langchain/retrievers/multi_query";
import "faiss-node";
import * as dotenv from "dotenv";

dotenv.config();

async function run() {
  const directory = "./kongyiji";
  const embeddings = new OpenAIEmbeddings({
    configuration: {
      baseURL: "https://ai-yyds.com/v1",
    },
  });
  const vectorstore = await FaissStore.load(directory, embeddings);

  const model = new ChatOpenAI({
    configuration: {
      baseURL: "https://ai-yyds.com/v1",
    },
  });
  const retriever = MultiQueryRetriever.fromLLM({
    llm: model,
    retriever: vectorstore.asRetriever(3),
    queryCount: 3,
    verbose: true,
  });
  const res = await retriever.invoke("茴香豆是做什么用的");

  console.log(res);
}

run();

```

 `MultiQueryRetriever` 会 **对每一个 query 调用 vector store 的 retriever**，也就是，按照我们上面的参数，会生成 3 * 3 共九个文档结果。简单总结下，`MultiQueryRetriever` 是在 RAG 中 retriever 的前期就引入 llm 对语意的理解能力，来解决纯粹的相似度搜索并不理解语意导致的问题。 

 **`Document Compressor`**  

```js
import { FaissStore } from "@langchain/community/vectorstores/faiss";
import { OpenAIEmbeddings, ChatOpenAI } from "@langchain/openai";
import { LLMChainExtractor } from "langchain/retrievers/document_compressors/chain_extract";
import { ContextualCompressionRetriever } from "langchain/retrievers/contextual_compression";

import * as dotenv from "dotenv";

dotenv.config();
// process.env.LANGCHAIN_VERBOSE = "true";

async function run() {
  const directory = "./kongyiji";
  const embeddings = new OpenAIEmbeddings({
    configuration: {
      baseURL: "https://ai-yyds.com/v1",
    },
  });
  const vectorstore = await FaissStore.load(directory, embeddings);

  const model = new ChatOpenAI({
    configuration: {
      baseURL: "https://ai-yyds.com/v1",
    },
  });
  const compressor = LLMChainExtractor.fromLLM(model);

  const retriever = new ContextualCompressionRetriever({
    baseCompressor: compressor,
    baseRetriever: vectorstore.asRetriever(2),
  });
  const res = await retriever.invoke("茴香豆是做什么用的");
  console.log(res);
}

run();
//
[
  Document {
    pageContent: '温两碗酒，要一碟茴香豆。',
    metadata: { source: '../data/kong.txt', loc: [Object] }
  }
]
```



 如果我们设置 k（每次检索返回的文档数）较小，因为自然语言的特殊性，可能相似度排名较高的并不是答案，就像搜索引擎依靠的也是相似性的度量，但排名最高的并不一定是最高质量的答案。而如果我们设置的 k 过大，就会导致大量的文档内容，可能会撑爆 llm 上下文窗口。 

就是根据用户提问从文档中提取出最相关的部分，并且强调不要让 LLM 去改动提取出来的部分，来避免 LLM 发挥自己的幻想改动原文。 



#####  Memory 

 聊天记录是一种特殊的上下文，让 llm 理解之前的沟通内容，方便理解用户意图。  llm 是无状态的，它并不会存储我们的聊天历史，每次都是根据上下文生成回答，聊天记录就是我们自己存储，并且作为传递给 llm 的上下文的一部分。 

```js
import { ChatOpenAI } from "@langchain/openai";
import { BufferMemory } from "langchain/memory";
import { ConversationChain } from "langchain/chains";

import * as dotenv from "dotenv";

dotenv.config();

async function main() {
  const chatModel = new ChatOpenAI({
    configuration: {
      baseURL: "https://ai-yyds.com/v1",
    },
  });
  const memory = new BufferMemory();
  const chain = new ConversationChain({ llm: chatModel, memory: memory });
  const res1 = await chain.call({ input: "我是小明" });
  console.log(res1);
  const res2 = await chain.call({ input: "我叫什么？" });
  console.log(res2);
}

main();
//
{ response: '你好小明，很高兴认识你！我是一个人工智能，可以回答你的问题和提供帮助。你有什么想知道的吗？' }
{ response: '你叫小明。你刚才告诉我你的名字啦！有什么其它问题想问吗？' }
```

