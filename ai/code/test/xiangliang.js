import { TextLoader } from "langchain/document_loaders/fs/text";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { OpenAIEmbeddings } from "@langchain/openai";
import { OpenAI } from "@langchain/openai";
import * as dotenv from "dotenv";
import { SentenceTransformer } from "@tuesdaycrowd/sentence-transformers";

dotenv.config();

const model = new OpenAI({
  temperature: 0,
  configuration: {
    baseURL: "https://ai-yyds.com/v1",
    apiKey: process.env.OPENAI_API_KEY, // 确保 API 密钥已设置
  },
});

async function main() {
  try {
    // 加载预训练的 SentenceTransformer 模型
    const sentenceModel = await SentenceTransformer.from_pretrained(
      "mixedbread-ai/mxbai-embed-large-v1"
    );

    // 要向量化的文本
    const text = "帮我给猫咪想三个可以注册的域名?";
    const loader = new TextLoader("kong.txt");
    const docs = await loader.load();

    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 100,
      chunkOverlap: 20,
    });

    const splitDocs = await splitter.splitDocuments(docs);

    // 编码文本
    const sentenceEmbedding = await sentenceModel.encode([text]);

    // 输出向量化结果
    console.log("Sentence Embedding:", sentenceEmbedding);

    // // 使用 OpenAI 模型进行进一步处理
    // const prompt = `帮我给{product}想三个可以注册的域名?`;
    // const response = await model.invoke(prompt);
    // console.log("Model Response:", response);

    console.log(splitDocs);
  } catch (error) {
    console.error("Error during processing:", error);
  }
}

main();
