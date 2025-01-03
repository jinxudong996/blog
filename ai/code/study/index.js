require('dotenv').config();

// 加载环境变量
const OPENAI_API_KEY = process.env.OPENAI_KEY;
const OPENAI_API_BASE = process.env.OPENAI_API_BASE;

const { ChatOpenAI } = require("@langchain/openai");
const { HumanMessage, SystemMessage } = require("@langchain/core/messages");
console.log(OPENAI_API_KEY)
console.log(OPENAI_API_BASE)
const model = new ChatOpenAI({ 
  model: "gpt-4o-mini",
  apiKey: OPENAI_API_KEY,
  baseUrl: OPENAI_API_BASE
});

const messages = [
  new SystemMessage("讲个笑话"),
  new HumanMessage("你好!"),
];

async function run() {
  try {
    console.log('开始调用模型')
    const response = await model.invoke('讲个笑话');
    console.log('有返回了')
    console.log(response);
  } catch (error) {
    console.error('Error invoking model:', error);
  }
}

run();