require('dotenv').config();
const { Configuration, OpenAIApi } = require('openai');

const configuration = new Configuration({
  apiKey: process.env.OPENAI_KEY,
  basePath: process.env.OPENAI_API_BASE,
});

const openai = new OpenAIApi(configuration);

const messages = [
  { role: "user", content: "介绍下你自己" }
];

async function getChatCompletion() {
  try {
    const res = await openai.createChatCompletion({
      model: "gpt-4-1106-preview",
      messages: messages,
      stream: false,
    });

    console.log(res.data.choices[0].message.content);
  } catch (error) {
    console.error("Error fetching chat completion:", error);
  }
}

getChatCompletion();