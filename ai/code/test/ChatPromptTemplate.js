import { ChatOpenAI } from "@langchain/openai";
import { SystemMessage, HumanMessage, AIMessage } from "@langchain/core/messages";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
    apiKey: process.env.OPENAI_API_KEY, // 确保 API 密钥已设置
  }
});

// 创建 SystemMessage, HumanMessage, AIMessage 实例
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

(async () => {
  try {
    // 格式化提示
    const formattedChatPrompt = await chatPrompt.formatMessages({});
    console.log(formattedChatPrompt);

    // 调用模型
    const response = await model.invoke(formattedChatPrompt);
    console.log(response.content);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();