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

// // 定义模板字符串
// const template = "你是一个{name},帮我起1个具有{county}特色的{sex}名字";

// // 替换占位符
// function formatPrompt(template, variables) {
//   return template.replace(/{([^}]+)}/g, (match, key) => variables[key] || match);
// }

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

    // const formattedPrompt = formatPrompt(template, variables);
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