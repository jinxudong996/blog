import { TextLoader } from "langchain/document_loaders/fs/text";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { OpenAIEmbeddings } from "@langchain/openai";
import { MemoryVectorStore } from "langchain/vectorstores/memory";

import * as dotenv from "dotenv";

const loader = new TextLoader("kong.txt");

dotenv.config();
async function main() {
  const docs = await loader.load();

  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 100,
    chunkOverlap: 20,
  });

  const splitDocs = await splitter.splitDocuments(docs);
  // console.log(splitDocs);

  const embeddings = new OpenAIEmbeddings({
    configuration: {
      baseURL: "https://ai-yyds.com/v1",
    },
  });

  // const res = await embeddings.embedQuery(splitDocs[0].pageContent);
  // console.log(res);
  const vectorstore = new MemoryVectorStore(embeddings);
  await vectorstore.addDocuments(splitDocs);
  const retriever = vectorstore.asRetriever(2);
  const res = await retriever.invoke("下酒菜一般是什么？");
  console.log(res);
}
main();
