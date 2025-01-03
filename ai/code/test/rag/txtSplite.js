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
// const model = new ChatOpenAI({
//   configuration: {
//     baseURL: OPENAI_API_BASE,
//     apiKey: OPENAI_API_KEY,
//   },
//   modelName: OPENAI_MODEL,
// });

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
