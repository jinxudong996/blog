import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "@langchain/core/messages";
import { PromptTemplate, FewShotPromptTemplate } from "@langchain/core/prompts";
import { LengthBasedExampleSelector } from "@langchain/core/example_selectors";
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
    apiKey: process.env.OPENAI_API_KEY, // 确保 API 密钥已设置
  }
});

// 定义示例组
const examples = [
  { input: "happy", output: "sad" },
  { input: "tall", output: "short" },
  { input: "energetic", output: "lethargic" },
  { input: "sunny", output: "gloomy" },
  { input: "windy", output: "calm" },
];

// 构造提示词模板
const examplePrompt = new PromptTemplate({
  template: "Input: {input}\nOutput: {output}",
  inputVariables: ["input", "output"],
});

// 调用长度示例选择器
const exampleSelector = new LengthBasedExampleSelector(
  [
    { input: "happy", output: "sad" },
    { input: "tall", output: "short" },
    { input: "energetic", output: "lethargic" },
    { input: "sunny", output: "gloomy" },
    { input: "windy", output: "calm" }
  ],{
    examples,
  examplePrompt,
  maxLength: 100,
});

// 使用小样本提示词模板来实现动态示例的调用
const dynamicPrompt = new FewShotPromptTemplate({
  exampleSelector,
  examplePrompt,
  prefix: "这里啥也没有",
  suffix: "Input: {adjective}\nOutput:",
  inputVariables: ["adjective"],
});
(async () => {
  try {
    // 调试信息：打印选择的示例
    const selectedExamples = await exampleSelector.selectExamples({ adjective: "开心" });
    console.log("Selected Examples:", selectedExamples);

    const formattedPrompt = await dynamicPrompt.format({ adjective: "开心" });
    console.log("Formatted Prompt:", formattedPrompt);

    const response = await model.invoke([
      new HumanMessage(formattedPrompt)
    ]);
    console.log("Model Response:", response.content);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();