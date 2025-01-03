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
    apiKey: process.env.OPENAI_API_KEY, // 确保 API 密钥已设置
  }
});

// 定义模板字符串
// const template = "你是一个{name},帮我起1个具有{county}特色的{sex}名字";
const templatePath = path.resolve(path.dirname(new URL(import.meta.url).pathname), 'template.txt')
console.log(templatePath)
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