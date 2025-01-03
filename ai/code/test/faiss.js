import { FaissStore } from "@langchain/community/vectorstores/faiss";
import { OpenAIEmbeddings } from "@langchain/openai";
import "faiss-node";

import * as dotenv from "dotenv";

dotenv.config();

const directory = "./kongyiji";
const embeddings = new OpenAIEmbeddings({
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
  },
});

async function run() {
  const vectorstore = await FaissStore.load(directory, embeddings);

  const retriever = vectorstore.asRetriever();
  const res = await retriever.invoke("茴香豆是做什么用的");

  console.log(res);
}

run();
