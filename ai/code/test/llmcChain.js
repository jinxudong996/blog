import { OpenAI } from "@langchain/openai";
import * as dotenv from "dotenv";

// 加载环境变量
dotenv.config();

const model = new OpenAI({
  temperature:0,
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
    // apiKey: "sk-uK6mnTkdB4TT6EAODf1a24Da7a43456793B1C12a61D4D167", // 确保 API 密钥已设置
  },
});

(async () => {
  try {
    const prompt_template = "帮我给{product}想三个可以注册的域名?"
    llm_chain = LLMChain(
      llm=llm,
      prompt=PromptTemplate.from_template(prompt_template),
      verbose=True,#是否开启日志
    )
    const response = await model.invoke(prompt);
    console.log(response);
  } catch (error) {
    console.error("Error invoking the model:", error);
  }
})();
