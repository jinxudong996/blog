import { FaissStore } from "@langchain/community/vectorstores/faiss";
import { OpenAIEmbeddings } from "@langchain/openai";
import { ScoreThresholdRetriever } from "langchain/retrievers/score_threshold";

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

  const retriever = ScoreThresholdRetriever.fromVectorStore(vectorstore, {
    minSimilarityScore: 0.45,
    maxK: 5,
    kIncrement: 1,
  });
  const res = await retriever.invoke("茴香豆是做什么用的");
  console.log(res);
}

run();
