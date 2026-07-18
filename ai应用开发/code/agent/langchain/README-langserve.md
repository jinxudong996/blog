# LangServe Runnable API

这个小案例把 `Prompt -> ChatOpenAI -> StrOutputParser` 组成的 Runnable 发布成 HTTP API，供 Web 页面调用。

## 安装依赖

在项目根目录执行：

```powershell
.\.venv\Scripts\python.exe -m pip install -r agent\langchain\requirements-langserve.txt
```

程序默认读取 `agent/.ENV`，需要包含：

```dotenv
LLM_MODEL_ID=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_API_KEY=你的密钥
LLM_TIMEOUT=60
```

## 启动服务

```powershell
cd agent\langchain
..\..\.venv\Scripts\python.exe -m uvicorn langserve_app:app --reload --host 127.0.0.1 --port 8000
```

启动后可以访问：

- API 文档：<http://127.0.0.1:8000/docs>
- LangServe Playground：<http://127.0.0.1:8000/chat/playground/>
- 健康检查：<http://127.0.0.1:8000/health>

## Web 调用

普通请求：

```javascript
const response = await fetch("http://127.0.0.1:8000/chat/invoke", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    input: { message: "用三句话介绍 LangServe" }
  })
});

const data = await response.json();
console.log(data.output);
```

对应的 `curl` 请求：

```powershell
curl.exe -X POST http://127.0.0.1:8000/chat/invoke `
  -H "Content-Type: application/json" `
  -d '{"input":{"message":"用三句话介绍 LangServe"}}'
```

LangServe 还会自动生成 `/chat/stream`、`/chat/batch`、`/chat/input_schema` 和 `/chat/output_schema` 等接口。生产环境请把代码中的 `allow_origins=["*"]` 改为实际 Web 域名。

## 流式输出

模型已开启 `streaming=True`。调用 `POST /chat/stream` 时，LangServe 会使用 SSE 持续返回生成片段，而不是等待完整回答生成后一次性返回。

浏览器调用示例见 `web_stream_example.html`。启动后端后直接打开该页面，点击“流式发送”即可看到逐步输出；点击“停止”会通过 `AbortController` 中断当前请求。

也可以使用命令行测试，`-N` 表示立即显示收到的数据：

```powershell
curl.exe -N -X POST http://127.0.0.1:8000/chat/stream `
  -H "Content-Type: application/json" `
  -d '{"input":{"message":"写一首关于程序员的短诗"}}'
```
