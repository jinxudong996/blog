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

// 自定义 LengthBasedExampleSelector
class CustomLengthBasedExampleSelector extends LengthBasedExampleSelector {
  async selectExamples(inputVariables) {
    let selectedExamples = [];
    let currentLength = 0;

    for (const example of this.examples) {
      const formattedExample = await this.examplePrompt.format(example);
      const exampleLength = formattedExample.length;

      console.log(`Formatted Example: ${formattedExample}`);
      console.log(`Example Length: ${exampleLength}`);

      if (currentLength + exampleLength <= this.maxLength) {
        selectedExamples.push(example);
        currentLength += exampleLength;
      } else {
        break;
      }
    }

    return selectedExamples;
  }
}

// 使用自定义的 LengthBasedExampleSelector
const exampleSelector = new CustomLengthBasedExampleSelector({
  examples,
  examplePrompt,
  maxLength: 100, // 增加 maxLength
});

// 使用小样本提示词模板来实现动态示例的调用
const dynamicPrompt = new FewShotPromptTemplate({
  exampleSelector,
  examplePrompt,
  prefix: "Give the antonym of every input",
  suffix: "Input: {adjective}\nOutput:",
  inputVariables: ["adjective"],
});

(async () => {
  try {
    // 调试信息：打印选择的示例
    const selectedExamples = await exampleSelector.selectExamples({ adjective: "开心" });
    console.log("Selected Examples:", selectedExamples);

    // 调试信息：打印 dynamicPrompt 的内部状态
    console.log("Dynamic Prompt Prefix:", dynamicPrompt.prefix);
    console.log("Dynamic Prompt Suffix:", dynamicPrompt.suffix);
    console.log("Dynamic Prompt Input Variables:", dynamicPrompt.inputVariables);

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