import { OpenAI } from "@langchain/openai";
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const model = new OpenAI({
  configuration: {
    // apiKey: process.env.OPENAI_API_KEY, // 使用环境变量中的 API 密钥
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