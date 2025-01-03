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