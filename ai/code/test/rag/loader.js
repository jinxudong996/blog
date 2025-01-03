import { ChatOpenAI } from "@langchain/openai";
import { SystemMessage, HumanMessage, AIMessage } from "@langchain/core/messages";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import * as dotenv from 'dotenv';
import { JSONLoader } from "langchain/document_loaders/fs/json";

// 加载环境变量
dotenv.config();

console.log(process.env.OPENAI_API_KEY)

const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
    apiKey: 'sk-uK6mnTkdB4TT6EAODf1a24Da7a43456793B1C12a61D4D167', // 确保 API 密钥已设置
  }
});

(async () => {
  try {
    const loader = new JSONLoader("example.json");
    const docs = await loader.load();
    console.log("Loaded documents:", docs);

    // 假设文档内容需要被拼接成一个字符串
    const documentContent = docs.map(doc => doc.pageContent).join('\n');

    // 创建聊天提示模板
    const chatPromptTemplate = ChatPromptTemplate.fromMessages([
      new SystemMessage("You are a helpful assistant."),
      new HumanMessage(`Here is the document content: ${documentContent}`),
      new AIMessage("Please summarize the document.")
    ]);

    // 格式化聊天提示
    const formattedChatPrompt = await chatPromptTemplate.formatMessages();

    // 调用模型
    const response = await model.invoke(formattedChatPrompt);
    console.log("Model response:", response);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();