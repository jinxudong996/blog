import { ChatOpenAI } from "@langchain/openai";
import { BufferMemory } from "langchain/memory";
import { ConversationChain } from "langchain/chains";

import * as dotenv from "dotenv";

dotenv.config();

async function main() {
  const chatModel = new ChatOpenAI({
    configuration: {
      baseURL: "https://ai-yyds.com/v1",
    },
  });
  const memory = new BufferMemory();
  const chain = new ConversationChain({ llm: chatModel, memory: memory });
  const res1 = await chain.call({ input: "我是小明" });
  console.log(res1);
  const res2 = await chain.call({ input: "我叫什么？" });
  console.log(res2);
}

main();
