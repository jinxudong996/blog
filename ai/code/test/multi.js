import { FaissStore } from "@langchain/community/vectorstores/faiss";
import { OpenAIEmbeddings, ChatOpenAI } from "@langchain/openai";
import { MultiQueryRetriever } from "langchain/retrievers/multi_query";
import "faiss-node";
import * as dotenv from "dotenv";

dotenv.config();

async function run() {
  const directory = "./kongyiji";
  const embeddings = new OpenAIEmbeddings({
    configuration: {
      baseURL: "https://ai-yyds.com/v1",
    },
  });
  const vectorstore = await FaissStore.load(directory, embeddings);

  const model = new ChatOpenAI({
    configuration: {
      baseURL: "https://ai-yyds.com/v1",
    },
  });
  const retriever = MultiQueryRetriever.fromLLM({
    llm: model,
    retriever: vectorstore.asRetriever(3),
    queryCount: 3,
    verbose: true,
  });
  const res = await retriever.invoke("茴香豆是做什么用的");

  console.log(res);
}

run();
