import { FaissStore } from "@langchain/community/vectorstores/faiss";
import { OpenAIEmbeddings, ChatOpenAI } from "@langchain/openai";
import { LLMChainExtractor } from "langchain/retrievers/document_compressors/chain_extract";
import { ContextualCompressionRetriever } from "langchain/retrievers/contextual_compression";

import * as dotenv from "dotenv";

dotenv.config();
// process.env.LANGCHAIN_VERBOSE = "true";

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
  const compressor = LLMChainExtractor.fromLLM(model);

  const retriever = new ContextualCompressionRetriever({
    baseCompressor: compressor,
    baseRetriever: vectorstore.asRetriever(2),
  });
  const res = await retriever.invoke("茴香豆是做什么用的");
  console.log(res);
}

run();
