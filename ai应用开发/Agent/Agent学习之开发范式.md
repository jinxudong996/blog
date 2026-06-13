#### 一、初识智能体

在人工智能领域，智能体被定义为任何可以通过传感器感知其所处环境，并自主地通过执行器采取行动以达成目的的实体。

这个定义包含了智能体存在的四个基本要素，环境就是智能体所处的外部世界，智能体通过它的传感器持续的感知环境状态，获取信息后，通过执行器来改变环境的状态，然后通过智能体的自主性来进行独立决策，从而达成设计目的。

当然智能体这个词并不是最近才出现的，最开始他们被称之为反射智能体，他们的决策核心被工程师设计的条件-动作规则构成，比如自动恒温器，若传感器感知室内的温度高于设定值就启动制冷系统。这种智能体完全依赖于当前对于环境的感知，不具备记忆和预测能力，如果环境的状态不足以作为决策的全部依据，智能体该怎么办？

虽有又出现了基于模板的反射智能体和基于目的的智能体，前者的智能体在内部有一个世界模型，用于追踪和理解环境中那些无法被直接感知的方面，这个模型让智能体有了初级的记忆，使其决策不再仅仅依赖于瞬间的感知，而是基于一个更加连贯、更加完整的世界状态理解；后者它的行为不再被动的对环境做出反应，而是主动的、有预见性地选择能够导向某个特定未来状态的行动。

当出现多个目标需要权衡时，又出现了基于效用的智能体，为每个可能的世界状态都赋予一个效用值，这个值代表了满地度的高低；而后有出现了学习型智能体，包含一个性能元件和一个学习元件， 学习元件通过观察性能元件在环境中的行动所带来的结果来不断修正性能元件的决策策略。 

而后随着以GPT为代表的大语言模型的出现，由大语言模型驱动的LLM智能体，其核心决策机制与传统的智能体有着本质的区别：基于预训练模型的推理引擎，可以从海量的非结构化数据中学习知识，能够理解高层级、模糊的自然语言，有着强大的涌现能力和泛化能力。



#### 二、智能体经典范式构建

一个现代的智能体，其核心能力在于能将大模型的推理能力与外部世界联通，能够自主的理解用户意图、拆解复杂任务，并通过调用代码解释器、搜索引擎、API等一些列工具，来获取信息、执行操作。同样大模型本身的幻觉、在复杂任务中可能会陷入循环推理、以及对工具的错误使用等，也构成了智能体的能力边界。

##### ReAct

ReAct是由Shunyu Yao于2022年提出的，其核心思想是模仿人类解决问题的方式，将推理 (Reasoning)与行动 (Acting)显式地结合起来，形成一个“思考-行动-观察”的循环。 

在ReAct诞生之前，主流的方法可以分为两类：一类是纯思考型，引导模型进行复杂的路基推理，但无法与外部世界交互，很容易产生幻觉；另一类是纯行动型，直接输出要执行的动作，缺少规划和纠错能力。

###### 核心组件

ReAct的巧妙之处在于，它认识到思考与行动是相辅相成的，思考指导行动，行动的结果又反过来修正思考。为此ReAct通过一种特殊的提示工程来引导模型，使其每一步的输出都遵循一个固定的轨迹。

- Thougth：思考组件，这是智能体的内心独白，会分析当前的情况、分解任务、指定下一步计划，或者反思上一步的结果
- Action：行动组件，这是智能体决定采取的具体行动，通常是调用一个外部工具
- Observation：观察组件，这是执行Action后从外部工具返回的结果，例如搜索结果的摘要或者API的返回值

智能体会不断的重复 `Thought → Action → Observation → Thought → ...` ，将新的观察结果追加到历史记录中，形成一个不断增长的上下文，指导Thoutght中认为已经找到了最终的答案，然后输出结果。这个过程形成了一个强大的协同效应，推理使得行动更具有目的性，而行动则为推理提供了事实依据。

![](https://static001.geekbang.org/resource/image/28/28/2893afa77f3b1ba4b477888e6c291a28.png?wh=2198x938)

接下来使用代码来近距离的观察下这三个核心组件

1. 思考组件

   在ReAct中，思考组件就是决策器、控制器，主要负责当去上下文，获取上一轮的观察结果，然后去考虑下一步去做什么，要不要使用工具、用啥工具、参数是啥，当信息足够收敛就输出Final。

   更加具体点，可以归纳为这几步：

   - 状态读取：把对话历史、任务目标、上一轮的observation结构化的数据读取进来
   - 工具路由：在工具集合中选择最合适的那个
   - 参数生产：将自然语言转换为工具的参数
   - 策略与约束：规定步数上限、重复次数、预算控制，避免重复调用同一工具
   - 收敛判断：拿到足够的信息就停止，避免工具重复循环
   - 错误处理：工具失败时，重试或者换工具，来兜底操作

   看下这个简单的实例

   ```python
   class ReasoningModule:
   
       def decide(self, query: str, observations: list[Observation]) -> tuple[str, Action]:
           # ---- 1) 先“读” observation（这一步是 reasoning 最容易做差的地方）
           if observations:
               last = observations[-1]
               if not last.ok:
                   thought = f"上一次工具调用失败({last.tool_name})，先给用户说明并停止。"
                   return thought, Action(type="final", final_answer=f"工具执行/解析失败：{last.error}，我先停止。")
   
               # 如果上一轮已经拿到足够信息，就收敛输出 final
               if last.tool_name == "get_current_weather":
                   thought = "已经获取到天气信息，直接组织最终回答。"
                   summary = last.parsed.get("summary", "")
                   return thought, Action(type="final", final_answer=summary)
   
               if last.tool_name == "calculator":
                   thought = "已经计算完成，直接返回结果。"
                   return thought, Action(type="final", final_answer=last.parsed.get("summary", "计算完成"))
   
           # ---- 2) 再决定要不要用工具，以及选哪个工具
           q = query.strip()
   
           # 规则：问天气就调用天气工具
           if "天气" in q:
               location = "北京" if "北京" in q else "上海" if "上海" in q else "你所在城市"
               thought = f"用户在问天气，调用 get_current_weather(location={location}) 获取实时信息。"
               return thought, Action(type="tool", tool_name="get_current_weather", tool_args={"location": location})
   
           # 规则：能识别出简单算式就调用计算器
           if any(ch.isdigit() for ch in q) and any(op in q for op in ["+", "-", "*", "/"]):
               expr = self._extract_expression(q)
               thought = f"用户像是在求值，调用 calculator(expression={expr})。"
               return thought, Action(type="tool", tool_name="calculator", tool_args={"expression": expr})
   
           # 否则直接回答
           thought = "不需要工具，直接回答。"
           return thought, Action(type="final", final_answer="我可以帮你查天气或做简单计算，你可以直接问：上海天气怎么样？或 12*(3+4)=多少")
   
       def _extract_expression(self, text: str) -> str:
           allowed = set("0123456789+-*/(). ")
           expr = "".join(ch for ch in text if ch in allowed).strip()
           return expr or text
   ```

   这个类就是用的是“规则推理”来模拟思考，可以更加直观的理解思考组件的作用： 
   首先定义了`decide`方法，这个方法第一个入参是当前对象的实例，第二个入参就是用户的提问，比如“上海天气怎么样”，第二个observations是一个已经发生过的工具调用的历史结果，每一个item需要有调用的工具名称，调用结果是否成功，调用的结构化输出，当然还有调用的失败的原因；然后就先获取上一个执行的结果last，然后判断结果的状态来，来决定下一步的执行，比如继续调用工具、调用计算器、直接返回结果，当然这里都是通过字符串匹配，在实际的agent中这里都是大模型来判断的。

   类中的第二个方法，是从用户的提问中抽离出需要的参数，调用是在当判断用户需要计算器时，通过正则来匹配出需要的数字的。

2. 行动组件

   行动组件就是将思考组件的决定真正的落地执行，将结果交给观察组件。

   行动组件一般做这些事情：

   - 工具注册

     维护一个TOOLS映射，就是工具名映射到具体的可调用的方法，同时还会检查工具是否存在、参数是否完整

   - 参数校验与类型转换

     将模型声测还能更多参数做校验，看是否缺字段、类型是否正确、值是否合法，必要的时候会做一些修正，比如检查城市的名称是否标准

   - 执行封装

     调用统一的入口：execute(action)，支持不同类型的工具，比如本地的方法，第三方的API，还有数据库之类的

   - 可靠性校验

     会检查执行的时间，比如超时控制、重试的次数，还有一些并发控制，比如熔断、限流，在搜索和查询时还会做一些缓存

   - 安全性检查

     会将参数消毒，防止SQL注入，过滤掉敏感信息，比如token、密码之类的返回给模型

   回到我们的demo，前面的思考组件decide的返回，就是执行的行动组件，比如

   ```python
    return thought, Action(type="final", final_answer=summary)
   ```

   

3. 观察组件

   观察组件就是将行动组件的执行结果，转换成结构化、可控、可回填给思考组件的信息，工具输出往往很长，很多脏数据，如果直接丢给思考组件喂给大模型，会导致成本高、噪声大、决策不稳定，这就需要观察组件来做数据清洗和归一化。

   观察组件一般会分为三层：

   - Collect

     这里会记录工具调用的过程、结果，比如工具名、参数、耗时，来保证agent的可观测性、可回放和可评估

   - Parse

     解析工具调用的结果，比如文本、日志使用正则抽离出可用信息，网页就提取标题、正文等关键字段

   - Normalize

     标准化就是统一字段命名、截断长文本、去噪

   看下代码：

   ```python
   class ObservationModule:
       """观察组件：采集(action结果) + 解析(raw->structured) + 标准化(schema)。"""
   
       def collect_and_parse(self, *, tool_name: str, args: dict[str, Any], raw_output: str, latency_ms: int) -> Observation:
           now_ms = int(time.time() * 1000)
           obs = Observation(
               tool_name=tool_name,
               args=args,
               ok=True,
               timestamp_ms=now_ms,
               latency_ms=latency_ms,
               raw=raw_output,
           )
   
           try:
               if self._looks_like_json(raw_output):
                   obs.content_type = "application/json"
                   data = json.loads(raw_output)
                   obs.parsed = self._parse_json(tool_name, data)
               else:
                   obs.content_type = "text/plain"
                   obs.parsed = self._parse_text(tool_name, raw_output)
           except Exception as exc:  # noqa: BLE001
               obs.ok = False
               obs.parse_error = f"{type(exc).__name__}: {exc}"
               obs.parsed = {"summary": "解析失败，保留原始输出", "raw_excerpt": raw_output[:200]}
   
           return obs
   
       def _looks_like_json(self, s: str) -> bool:
           s = s.strip()
           return (s.startswith("{") and s.endswith("}")) or (s.startswith("[") and s.endswith("]"))
   
       def _parse_json(self, tool_name: str, data: Any) -> dict[str, Any]:
           """把 JSON 解析成 agent 更容易用的字段。"""
   
           if tool_name == "get_current_weather" and isinstance(data, dict):
               location = data.get("location")
               temperature = data.get("temperature")
               condition = data.get("condition")
               return {
                   "summary": f"{location} 当前 {condition}，温度 {temperature}",
                   "location": location,
                   "temperature": temperature,
                   "condition": condition,
               }
   
           # 默认：原样放入，外加一个简短 summary
           return {
               "summary": f"{tool_name} 返回 JSON（已解析）",
               "data": data,
           }
   
       def _parse_text(self, tool_name: str, text: str) -> dict[str, Any]:
           """解析半结构化文本：提取关键信息，避免把大段噪声塞回 LLM。"""
   
           if tool_name == "fetch_webpage":
               title = self._extract_title(text)
               keywords = self._extract_keywords(text)
               return {
                   "summary": f"网页抓取完成：{title or '未知标题'}",
                   "title": title,
                   "keywords": keywords,
                   "raw_excerpt": text[:240],
               }
   
           return {
               "summary": f"{tool_name} 返回文本（未做专用解析）",
               "raw_excerpt": text[:240],
           }
   
       def _extract_title(self, text: str) -> str | None:
           m = re.search(r"^TITLE:\s*(.+)$", text, flags=re.MULTILINE)
           if m:
               return m.group(1).strip()
           return None
   
       def _extract_keywords(self, text: str) -> list[str]:
           m = re.search(r"^KEYWORDS:\s*(.+)$", text, flags=re.MULTILINE)
           if not m:
               return []
           return [w.strip() for w in m.group(1).split(",") if w.strip()]
   ```

###### 案例

上面只是通过推理规则来模拟思考，接下来写一个真实的调用大模型的搜索agent。

首先封装一个调用大模型接口的类：

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

# 加载 .env 文件中的环境变量
load_dotenv()

class HelloAgentsLLM:
    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))
        
        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用大语言模型进行思考，并返回其响应。
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            
            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()  # 在流式输出结束后换行
            return "".join(collected_content)

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None

```

也比较简单，就两个方法，一个`__init__`就是初始化模型，传入模型地址和token，`think`也就是流失调用了下大模型。

在根目录写入配置文件

```
# 供 llm_client.py（OpenAI SDK）读取的配置
LLM_MODEL_ID=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_TIMEOUT=60

DEEPSEEK_API_KEY = sk-xxx
SERPAPI_API_KEY="xxx"
```

然后写个工具方法，搜索采用` SerpApi  `，这是一个通过API获取各大搜索引擎的结构化搜索结果，挺方便的，唯一的缺点就是收费，不过测试有一个月一百次的额度。需要前往 [SerpApi官网](https://serpapi.com/) 注册一个免费账户，获取你的API密钥，然后写入到根目录的配置文件中。

```python
def search(query: str) -> str:
    """
    一个基于SerpApi的实战网页搜索引擎工具。
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息。
    """
    print(f"🔍 正在执行 [SerpApi] 网页搜索: {query}")
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "错误：SERPAPI_API_KEY 未在 .env 文件中配置。"

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "gl": "cn",  # 国家代码
            "hl": "zh-cn", # 语言代码
        }
        
        client = SerpApiClient(params)
        results = client.get_dict()
        
        # 智能解析：优先寻找最直接的答案
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)
        
        return f"对不起，没有找到关于 '{query}' 的信息。"

    except Exception as e:
        return f"搜索时发生错误: {e}"
    
```

也比较简单，就是调用搜索接口，然后解析返回结果，在返回结果中检查是否存在 `answer_box`（Google的答案摘要框）或 `knowledge_graph`（知识图谱）等信息，如果存在，就直接返回这些最精确的答案。 

然后定义一个工具执行器来调度这些工具：

```python
class ToolExecutor:
    """
    一个工具执行器，负责管理和执行工具。
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        """
        向工具箱中注册一个新工具。
        """
        if name in self.tools:
            print(f"警告：工具 '{name}' 已存在，将被覆盖。")
        
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")

    def getTool(self, name: str) -> callable:
        """
        根据名称获取一个工具的执行函数。
        """
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        """
        return "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.tools.items()
        ])
```

这是一个工具的注册和调度的类，看下后续agent中的调用就明白了：

```python
 tool_executor = ToolExecutor()
 search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
 tool_executor.registerTool("Search", search_desc, search)
```

通过`registerTool`去注册工具，他的`tools`长这样：

```python
"Search": {
	"description": "一个网页搜索引擎…",
	"func": <function search>,
},
```

就是方法名：描述和具体的执行方法。

然后看下agent的主体结构：

```python
class ReActAgent:
    def __init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def run(self, question: str):
        self.history = []
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"\n--- 第 {current_step} 步 ---")

            tools_desc = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(tools=tools_desc, question=question, history=history_str)

            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)
            if not response_text:
                print("错误：LLM未能返回有效响应。"); break

            thought, action = self._parse_output(response_text)
            if thought: print(f"🤔 思考: {thought}")
            if not action: print("警告：未能解析出有效的Action，流程终止。"); break
            
            if action.startswith("Finish"):
                # 如果是Finish指令，提取最终答案并结束
                final_answer = self._parse_action_input(action)
                print(f"🎉 最终答案: {final_answer}")
                return final_answer
            
            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                self.history.append("Observation: 无效的Action格式，请检查。"); continue

            print(f"🎬 行动: {tool_name}[{tool_input}]")
            tool_function = self.tool_executor.getTool(tool_name)
            observation = tool_function(tool_input) if tool_function else f"错误：未找到名为 '{tool_name}' 的工具。"
            
            print(f"👀 观察: {observation}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        print("已达到最大步数，流程终止。")
        return None

    def _parse_output(self, text: str):
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        return (match.group(1), match.group(2)) if match else (None, None)

    def _parse_action_input(self, action_text: str):
        match = re.match(r"\w+\[(.*)\]", action_text, re.DOTALL)
        return match.group(1) if match else ""
```

首先`__init__`方法定义了`llm_client`连接大模型的流式输出的方法，`tool_executor`就是前面介绍的工具调度的方法，`max_steps`是循环的最大次数买这个一定要设置的，避免出现死循环导致token浪费，而`history`数组则是一个观察组件的日志缓冲区。

接下来就是核心的`run`方法，方法接受一个用户提问作为参数，然后就开始了循环，同时清空`history`数组和current_step，后者这个变量是记录当前步数的。首先获取当前的工具集合，然后组装一个完善的`prompt`，这个`prompt`是长这样：

```python
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下：
{tools}

请严格按照以下格式进行回应：

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`：调用一个可用工具。
- `Finish[最终答案]`：当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后使用 `Finish[最终答案]` 来输出最终答案。


现在，请开始解决以下问题：
Question: {question}
History: {history}
"""
```

一个标准的ReAct Prompt模板必须包含以下几点

- 角色定义：比如我们的，有能力调用外部工具的智能助手
- 严格约束流程：我们这里定义了Thought、Action
- 工具清单与格式：我们这里告诉他了可用的工具
- 输出格式强约束：我们这里是你必须在`Action:`字段后使用 `Finish[最终答案]` 来输出最终答案
- 停止条件：约定结束后就不在调用工具，我们这里`Finish[最终答案]`：当你认为已经获得最终答案时。

这里设置`Prompt`非常的繁琐，原因也很简单，我们这里的ReAct几乎没有智能，智能主要来自于LLM，所以就需要设置一套严格的`Prompt`来约束LLM：输出必须要可解析，我们这里通过正则来解析思考组件和行动组件，工具调用要受控，我们这里只允许`Tool[input]`和`Finish[]`；我们这里将观察的`History`数组拼接到`Prompt`中，然后约束模型必须先看行动组件在决定下一步。

代码中先将组装的`Prompt`喂给大模型，得到一个包含Thought和Action的输出，调用`_parse_output`将他们解析出来，如果`action`是以`Finish`开头的，就表明我们获得了最终更多结果，之所以这样是因为我们在提示词中约束大模型：你必须在`Action:`字段后使用 `Finish[最终答案]` 来输出最终答案。如果没有`Finish`字段，就表明还需要进一步的循环，然后将解析的action和observation塞到`history`数组中，然后继续重复这个步骤。

还记得开头定义的`ReAct`范式的三个核心组件嘛：Thought组件是LLM思考的结果，Action组件是调用何种工具，Observation组件是工具调用的输出，这里也是按照这个范式来做的，在`History`数组中添加Action和Thought，给大模型看到工具调用的输出，其实我这里有个疑问，为啥不将Thought也给大模型，问了下大模型，结论是这样的，Thought是不稳定、冗余的输出，可能会很长，会迅速的将上下文窗口占满，而Action和Observation，是客观客可复用的外部事实，调用了啥工具，工具的输出都是确定的，这是下一轮推理的刚需，而且可以被模型稳定的利用。

调用是这样的

```python
agent = ReActAgent(llm_client=llm, tool_executor=tool_executor)
question = "华为最新的手机是哪一款？它的主要卖点是什么？"
agent.run(question)
```

看下我们的输出：

```
工具 'Search' 已注册。

--- 第 1 步 ---
🧠 正在调用 deepseek-chat 模型...
✅ 大语言模型响应成功:
Thought: 用户询问华为最新的手机是哪一款以及其主要卖点。我需要查找关于华为最新发布手机的信息。由于手机型号更新很快，我的知识可能不是最新
的，所以我应该使用搜索引擎来获取准确和最新的信息。

Action: Search[华为最新手机 型号 主要卖点]
🤔 思考: 用户询问华为最新的手机是哪一款以及其主要卖点。我需要查找关于华为最新发布手机的信息。由于手机型号更新很快，我的知识可能不是最新
的，所以我应该使用搜索引擎来获取准确和最新的信息。
🎬 行动: Search[华为最新手机 型号 主要卖点]
🔍 正在执行 [SerpApi] 网页搜索: 华为最新手机 型号 主要卖点
👀 观察: [1] 2026年华为手机哪一款性价比高？华为手机推荐与市场分析
现在华为手机最大的卖点只剩下鸿蒙HarmonyOS系统，以及饱受争议的品牌信仰。 这里推荐目前值得入手的几款华为系列手机，根据不同预算自行选择：. 华为目前最受欢迎，也是搭载 ...

[2] 旗舰手机产品市场盘点月报
华为P60在营销中主要以外观及参数升级为主要卖点，包括机身设计工艺、摄影、耐摔、效率方面。从用户电. 商评论来看，产品在发热、指纹识别灵敏度
、续航等方面仍需要进行一定 ...

[3] 华为一口气发了22个新品被一款千元机抢了风头
... 系列，应该是要在中端走量机型上下手了。 华为一口气发了22个新品被一款千元机抢了. 要我说这台机器的主要卖点有三，麒麟8000 处理器，8500 
mAh 的大 ...

...

--- 第 4 步 ---
🧠 正在调用 deepseek-chat 模型...
✅ 大语言模型响应成功:
Thought: 用户询问华为最新的手机是哪一款以及其主要卖点。根据之前的搜索历史，我们尝试搜索了“华为最新手机 型号 主要卖点”，但返回的结果似乎
没有明确指出最新的具体型号。随后我们搜索了“华为最新旗舰手机 2024 主要卖点”，结果提到了华为Mate 70系列，并预计在2024年10月发布。为了确认
Mate 70系列是否已经发布以及获取其确切的主要卖点，我们进一步搜索了“华为Mate 70 发布 主要卖点”。根据最新的搜索结果，特别是第一条“5499元起
！华为Mate70系列发布，最强Mate啥卖点？”，可以确认华为Mate 70系列已经发布。因此，目前华为最新的手机是华为Mate 70系列（包括Mate 70、Mate 
70 Pro、Mate 70 Pro+等型号）。其主要卖点包括AI功能（如AI影像、手势控制、隐私保护等），以及可能的外观设计、摄影能力等。现在我们已经收集 
到足够的信息来回答用户的问题。

Action: Finish[根据目前的信息，华为最新的手机是华为Mate 70系列（例如Mate 70、Mate 70 Pro、Mate 70 Pro+等）。其主要卖点集中在AI功能上， 
包括AI影像、手势控制和隐私保护等，这标志着AI已成为该系列的核心竞争力。此外，该系列可能还延续了华为在设计和摄影方面的优势。]
🤔 思考: 用户询问华为最新的手机是哪一款以及其主要卖点。根据之前的搜索历史，我们尝试搜索了“华为最新手机 型号 主要卖点”，但返回的结果似乎
没有明确指出最新的具体型号。随后我们搜索了“华为最新旗舰手机 2024 主要卖点”，结果提到了华为Mate 70系列，并预计在2024年10月发布。为了确认
Mate 70系列是否已经发布以及获取其确切的主要卖点，我们进一步搜索了“华为Mate 70 发布 主要卖点”。根据最新的搜索结果，特别是第一条“5499元起
！华为Mate70系列发布，最强Mate啥卖点？”，可以确认华为Mate 70系列已经发布。因此，目前华为最新的手机是华为Mate 70系列（包括Mate 70、Mate 
70 Pro、Mate 70 Pro+等型号）。其主要卖点包括AI功能（如AI影像、手势控制、隐私保护等），以及可能的外观设计、摄影能力等。现在我们已经收集 
🤔 思考: 用户询问华为最新的手机是哪一款以及其主要卖点。根据之前的搜索历史，我们尝试搜索了“华为最新手机 型号 主要卖点”，但返回的结果似乎
没有明确指出最新的具体型号。随后我们搜索了“华为最新旗舰手机 2024 主要卖点”，结果提到了华为Mate 70系列，并预计在2024年10月发布。为了确认
Mate 70系列是否已经发布以及获取其确切的主要卖点，我们进一步搜索了“华为Mate 70 发布 主要卖点”。根据最新的搜索结果，特别是第一条“5499元起
！华为Mate70系列发布，最强Mate啥卖点？”，可以确认华为Mate 70系列已经发布。因此，目前华为最新的手机是华为Mate 70系列（包括Mate 70、Mate 
70 Pro、Mate 70 Pro+等型号）。其主要卖点包括AI功能（如AI影像、手势控制、隐私保护等），以及可能的外观设计、摄影能力等。现在我们已经收集 
Mate 70系列是否已经发布以及获取其确切的主要卖点，我们进一步搜索了“华为Mate 70 发布 主要卖点”。根据最新的搜索结果，特别是第一条“5499元起
！华为Mate70系列发布，最强Mate啥卖点？”，可以确认华为Mate 70系列已经发布。因此，目前华为最新的手机是华为Mate 70系列（包括Mate 70、Mate 
70 Pro、Mate 70 Pro+等型号）。其主要卖点包括AI功能（如AI影像、手势控制、隐私保护等），以及可能的外观设计、摄影能力等。现在我们已经收集 
70 Pro、Mate 70 Pro+等型号）。其主要卖点包括AI功能（如AI影像、手势控制、隐私保护等），以及可能的外观设计、摄影能力等。现在我们已经收集 
到足够的信息来回答用户的问题。
🎉 最终答案: 根据目前的信息，华为最新的手机是华为Mate 70系列（例如Mate 70、Mate 70 Pro、Mate 70 Pro+等）。其主要卖点集中在AI功能上，包 
括AI影像、手势控制和隐私保护等，这标志着AI已成为该系列的核心竞争力。此外，该系列可能还延续了华为在设计和摄影方面的优势。
```

###### 案例二



可以看到ReAct范式的agent，对于LLM自身的能力有着很强的依赖性，如果LLM的逻辑推理能力、指令遵循能力或者格式化输出能力不足，就很容易在 在 `Thought` 环节产生错误的规划，或者在 `Action` 环节生成不符合格式的指令，导致整个流程中断；整个机制对于提示词有着非常强的依赖，提示词模板需要精心设计。















##### Plan-and-Solve

这种开发范式根据名称就可以确定：先规划、再执行。由 Lei Wang 在2023年提出 ，核心动机是为了解决思维链在处理多步骤、复杂问题时容易偏离轨道的问题。

其核心阶段可以分为两步：

1. Planning规划阶段，首先智能体会接收用户的完整问题，第一个任务不是直接去解决问题或者调用工具，而是将问题分解，制定出一个清晰、分步骤的行动计划，这个计划本身就是一次大模型调用的产物
2. Solving执行阶段，在获取完整的计划后，智能体进入执行阶段，会严格按照计划中的步骤，逐一执行，每一步的执行都可能是一次独立的LLM调用或者是对上一步结果的加工处理，直到计划中的所有步骤都完成。

首先这里就需要一个提示词，让大模型接受原始问题，然后输出一个清晰、分步骤的行动计划，这个计划必须是结构化的，以便我们的代码可以轻松解析并逐一执行，因此就需要通过提示词明确的告诉模型他的角色和任务，然后输出一个格式的范例。

接下来写一个小案例，更加直观的看下这种开发范式

按照前面说的，需要一个规划器和执行器，先需要对应的提示词：

首先看下规划器的提示词：

~~~python
PLANNER_PROMPT_TEMPLATE = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}

请严格按照以下格式输出你的计划，```python与```作为前后缀是必要的:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""
~~~

再将执行逻辑封装成一个类

```python
class Planner:
    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def plan(self, question: str) -> list[str]:
        prompt = PLANNER_PROMPT_TEMPLATE.format(question=question)
        messages = [{"role": "user", "content": prompt}]
        
        print("--- 正在生成计划 ---")
        response_text = self.llm_client.think(messages=messages) or ""
        print(f"✅ 计划已生成:\n{response_text}")
        
        try:
            plan_str = response_text.split("```python")[1].split("```")[0].strip()
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错: {e}")
            print(f"原始响应: {response_text}")
            return []
        except Exception as e:
            print(f"❌ 解析计划时发生未知错误: {e}")
            return []
```

这里就是将规划器的提示词喂给大模型，然后获取一个具体的步骤列表，最终的输出是这样：

```
["计算周二卖出的苹果数量：周一卖出的15个苹果乘以2", "计算周三卖出的苹果数量：周二卖
减去5个", "将周一、周二、周三卖出的苹果数量相加，得到三天的总销量"]
```

执行器的提示词：

```python
EXECUTOR_PROMPT_TEMPLATE = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决“当前步骤”，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对“当前步骤”的回答:
"""
```

然后封装一个执行器的类

```python
class Executor:
    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def execute(self, question: str, plan: list[str]) -> str:
        history = ""
        final_answer = ""
        
        print("\n--- 正在执行计划 ---")
        for i, step in enumerate(plan, 1):
            print(f"\n-> 正在执行步骤 {i}/{len(plan)}: {step}")
            prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                question=question, plan=plan, history=history if history else "无", current_step=step
            )
            messages = [{"role": "user", "content": prompt}]
            
            response_text = self.llm_client.think(messages=messages) or ""
            
            history += f"步骤 {i}: {step}\n结果: {response_text}\n\n"
            final_answer = response_text
            print(f"✅ 步骤 {i} 已完成，结果: {final_answer}")
            
        return final_answer
```

这里就遍历规划列表，然后记录下每个步骤的历史状态

有了执行器和规划器，就开始构建智能体

```python
class PlanAndSolveAgent:
    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client
        self.planner = Planner(self.llm_client)
        self.executor = Executor(self.llm_client)

    def run(self, question: str):
        print(f"\n--- 开始处理问题 ---\n问题: {question}")
        plan = self.planner.plan(question)
        if not plan:
            print("\n--- 任务终止 --- \n无法生成有效的行动计划。")
            return
        final_answer = self.executor.execute(question, plan)
        print(f"\n--- 任务完成 ---\n最终答案: {final_answer}")
```

调用

```python
try:
        llm_client = HelloAgentsLLM()
        agent = PlanAndSolveAgent(llm_client)
        question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
        agent.run(question)
    except ValueError as e:
        print(e)
```

看下输出的日志：

```
--- 开始处理问题 ---
问题: 一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。
请问这三天总共卖出了多少个苹果？
--- 正在生成计划 ---
🧠 正在调用 deepseek-chat 模型...
✅ 大语言模型响应成功:
​```python
["计算周二卖出的苹果数量：周一卖出的15个苹果乘以2", "计算周三卖出的苹果数量：周二卖出的数量减去5个
", "将周一、周二、周三卖出的苹果数量相加，得到三天的总销量"]
​```
✅ 计划已生成:
​```python
["计算周二卖出的苹果数量：周一卖出的15个苹果乘以2", "计算周三卖出的苹果数量：周二卖出的数量减去5个
", "将周一、周二、周三卖出的苹果数量相加，得到三天的总销量"]
​```

--- 正在执行计划 ---

-> 正在执行步骤 1/3: 计算周二卖出的苹果数量：周一卖出的15个苹果乘以2
🧠 正在调用 deepseek-chat 模型...
✅ 大语言模型响应成功:
30
✅ 步骤 1 已完成，结果: 30

-> 正在执行步骤 2/3: 计算周三卖出的苹果数量：周二卖出的数量减去5个
🧠 正在调用 deepseek-chat 模型...
✅ 大语言模型响应成功:
25
✅ 步骤 2 已完成，结果: 25

-> 正在执行步骤 3/3: 将周一、周二、周三卖出的苹果数量相加，得到三天的总销量
🧠 正在调用 deepseek-chat 模型...
✅ 大语言模型响应成功:
70
✅ 步骤 3 已完成，结果: 70

--- 任务完成 ---
最终答案: 70
```



##### Reflection

前面学习了ReAct和Plan-and-Solve范式，这两个范式中，智能体一旦完成了任务，他的工作流程就结束了，然后他们的初始答案、无论是行动轨迹还是最终结果，都可能存在谬误或者有改进的地方，`Reflection`机制的核心思想，就是为智能体引入一种事后的自我矫正循环，使其能够像人类一样，审视自己的工作，发现不足，进而迭代优化。

`Reflection`核心的工作流程可以概括为三步循环：执行 -> 反思 -> 优化

- 执行，首先智能体选用前面的开发范式，ReAct或者Plan-and-Solve去尝试完成任务，生成一个初步解决方案或者行动轨迹
- 反思，接着智能体进入反思阶段，会调用一个独立的、或者带有特殊提示词的大模型，来扮演评审员的角色
- 优化，最后智能体将初稿和反馈最为新的上下文，再次调用大模型，要求他根据反馈内容对初稿进行修正，生成一个更完善的修订稿。



#### 低代码构建









#### 开发框架构建智能体





本人**金旭东**  身份证号码420321199601088018

在职时间段：**2023 年 06 月 01 日 —2024 年 08 月 08 日**

本人原入职主体为北京东方融创信息技术有限公司，自**2023 年 6 月 1 日起**，工资发放、用工管理转为**北京东方融创信息技术有限公司上海分公司**，两家公司为关联总分公司，属于关联企业混同用工，本人工作岗位、工作地点未发生变更，劳动关系连续存续至 2024 年 08 月 08 日离职。

该上海分公司在职期间，未按本人实际税前工资基数足额缴存住房公积金，存在少缴、漏缴违规行为。

现诉求：

1、按本人实际全部税前工资收入为基数，补缴 2023.06.01–2024.08.08 期间住房公积金（单位部分 + 个人部分含利息）；

2、本人劳动合同、离职证明已遗失，可提供**上海社保明细、个税纳税记录、银行工资流水、总分公司工商关联资料**

本人**金旭东**

在职时间段：**2023 年 02 月 27 日 —2023 年 05 月 31 日**

本人于 2023 年 2 月 27 日入职，劳动合同主体为**北京东方融创信息技术有限公司**，在职前期 2023.02.27–2023.05.31 期间，由**北京东方融创信息技术有限公司**发放工资、代扣个人所得税，存在事实劳动关系。

单位在此期间未按本人实际工资基数足额缴存住房公积金，属于少缴、漏缴公积金行为。

现诉求：

1、按本人实际税前工资为基数，补缴 2023.02.27–2023.05.31 期间住房公积金（单位部分 + 个人部分含利息）；

2、本人已无劳动合同、离职证明，可提供**社保缴费记录、个人所得税纳税记录、银行工资流水、两家企业工商关联信息**







