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
  model: "gpt-4o",
  // model:"gpt-4-1106-preview",
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