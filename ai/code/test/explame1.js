import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "@langchain/core/messages";
import { PromptTemplate,FewShotPromptTemplate } from "@langchain/core/prompts";
import {LengthBasedExampleSelector} from "@langchain/core/example_selectors";
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const examples = [
  { input: "happy", output: "sad" },
  { input: "tall", output: "short" },
  { input: "energetic", output: "lethargic" },
  { input: "sunny", output: "gloomy" },
  { input: "windy", output: "calm" },
]

const model = new ChatOpenAI({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
    apiKey: process.env.OPENAI_API_KEY, // 确保 API 密钥已设置
  }
});
const exampleSelector = new LengthBasedExampleSelector(
  [ 
    { input: "happy", output: "sad" },
    { input: "tall", output: "short" },
    { input: "energetic", output: "lethargic" },
    { input: "sunny", output: "gloomy" },
    { input: "windy", output: "calm" },
  ],
  {
    examplePrompt: new PromptTemplate({
      inputVariables: ["input", "output"],
      template: "Input: {input}\nOutput: {output}",
    }),
    maxLength: 100,
});
const dynamicPrompt = new FewShotPromptTemplate({
  exampleSelector:exampleSelector,
  examplePrompt: new PromptTemplate({
    inputVariables: ["input", "output"],
    template: "Input: {input}\nOutput: {output}",
  }),
  prefix: "Give the antonym of every input",
  suffix: "Input: {adjective}\nOutput:",
  inputVariables: ["adjective"],
});

// console.log(dynamicPrompt.format({ adjective: "big" }));
const longString = "big and huge adn massive and large and gigantic and tall and much much much much much much bigger then everyone";
(async () => {
  try {
    const selectedExamples = await exampleSelector.selectExamples({ adjective: 123 });
    console.log("Selected Examples:", selectedExamples);
    const formattedPrompt = await dynamicPrompt.format({ adjective: longString });
    console.log(123)
    console.log(formattedPrompt);

    const response = await model.invoke([
      formattedPrompt
    ]);
    console.log(response.content);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();