# 故事结构化抽取器

这个项目把小说或故事片段转换为可校验的 `StoryBible`，同时保留每条声明的原文证据、来源类型和审核状态。最终的 `story_bible.json` 只包含证据已自动通过的结构，供下游使用；`extraction_report.json` 还包含模型的 `candidate_bible`、未发布原因以及完整声明账本。

## 运行

从项目根目录执行：

```powershell
python -m agent.langchain.story_bible_extractor input.txt
```

也可以从 `agent/langchain` 目录执行：

```powershell
python -m story_bible_extractor input.txt --output out/story_bible.json --report out/report.json
```

CLI 沿用仓库现有的 `agent/.ENV` 配置：`LLM_MODEL_ID`、`LLM_API_KEY`、`LLM_BASE_URL`。模型必须支持 LangChain 的结构化输出。

## 数据边界

- 只有带有能在原文中找到的精确 quote 的声明才可能被接受。
- 叙述事实自动接受；角色陈述和推断进入 `needs_review`。
- 同一 subject/predicate 出现多个不同值时，所有声明保留，并生成 unresolved conflict。
- 人物、关系和事件必须引用 `source_claim_ids`；引用缺失、被拒绝或待审核时不会发布到正式 StoryBible。
- 世界观摘要目前保留在 `candidate_bible`，不自动发布，避免无字段级证据的摘要进入事实层。
- `null` 表示未知标量，空列表表示没有抽取到集合成员。

## 测试

```powershell
python -m unittest discover -s agent/langchain/story_bible_extractor/tests -p "test_*.py"
```

测试不调用网络，覆盖证据校验、伪造引用拒绝和冲突分流。
