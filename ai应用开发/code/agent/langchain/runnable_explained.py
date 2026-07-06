"""
LangChain Runnable 基础类的核心实现解析
"""

# ============================================================================
# Runnable 基类的核心方法
# ============================================================================

# 1. invoke (抽象方法，必须实现)
# ============================================================================
def invoke(
    self,
    input: Input,
    config: RunnableConfig | None = None,
    **kwargs: Any,
) -> Output:
    """
    Transform a single input into an output.
    
    抽象方法，子类必须实现这个方法。
    这是最基础的执行方法。
    
    Args:
        input: 单个输入
        config: 运行配置（tags、metadata、max_concurrency 等）
        
    Returns:
        单个输出
    """
    pass


# 2. ainvoke (异步版本)
# ============================================================================
async def ainvoke(
    self,
    input: Input,
    config: RunnableConfig | None = None,
    **kwargs: Any,
) -> Output:
    """
    异步版本的 invoke。
    
    默认实现：使用 asyncio 的线程池执行器运行 invoke()
    
    可以被子类重写以提供原生异步实现。
    """
    return await run_in_executor(
        config, 
        self.invoke, 
        input, 
        config, 
        **kwargs
    )


# 3. batch (批处理)
# ============================================================================
def batch(
    self,
    inputs: list[Input],
    config: RunnableConfig | list[RunnableConfig] | None = None,
    *,
    return_exceptions: bool = False,
    **kwargs: Any | None,
) -> list[Output]:
    """
    对多个输入进行批处理。
    
    默认实现：使用线程池并行执行 invoke()
    
    如果底层有 API 支持批处理模式，子类应该重写此方法以优化性能。
    
    Args:
        inputs: 输入列表
        config: 可以是单个配置或配置列表
        return_exceptions: True 时返回异常而不是抛出
        
    Returns:
        输出列表
        
    工作流程:
    1. 如果输入为空，返回空列表
    2. 将 config 扩展为配置列表
    3. 定义 invoke 包装器（处理异常）
    4. 如果只有一个输入，直接调用（不用 executor）
    5. 否则使用线程池并行执行
    """
    # 简化的伪代码
    if not inputs:
        return []
    
    configs = get_config_list(config, len(inputs))
    
    # 如果只有一个输入，跳过 executor
    if len(inputs) == 1:
        return [self.invoke(inputs[0], configs[0], **kwargs)]
    
    # 使用线程池并行处理
    with get_executor_for_config(configs[0]) as executor:
        return list(
            executor.map(
                lambda inp, cfg: self.invoke(inp, cfg, **kwargs),
                inputs,
                configs
            )
        )


# 4. abatch (异步批处理)
# ============================================================================
async def abatch(
    self,
    inputs: list[Input],
    config: RunnableConfig | list[RunnableConfig] | None = None,
    *,
    return_exceptions: bool = False,
    **kwargs: Any | None,
) -> list[Output]:
    """
    异步批处理。
    
    默认实现：使用 asyncio.gather 并行执行 ainvoke()
    
    工作流程:
    1. 为每个输入创建 ainvoke() 协程
    2. 使用 gather_with_concurrency 控制并发数量
    3. 返回结果列表
    """
    configs = get_config_list(config, len(inputs))
    
    async def ainvoke_wrapper(value, config):
        if return_exceptions:
            try:
                return await self.ainvoke(value, config, **kwargs)
            except Exception as e:
                return e
        else:
            return await self.ainvoke(value, config, **kwargs)
    
    # 使用 gather_with_concurrency 尊重 max_concurrency 设置
    return await gather_with_concurrency(
        configs[0].get("max_concurrency"),
        *[ainvoke_wrapper(inp, cfg) for inp, cfg in zip(inputs, configs)]
    )


# 5. stream (流式输出)
# ============================================================================
def stream(
    self,
    input: Input,
    config: RunnableConfig | None = None,
    **kwargs: Any | None,
) -> Iterator[Output]:
    """
    流式输出。
    
    默认实现：只调用一次 invoke() 并 yield 结果。
    
    子类应该重写此方法以实现真正的流式输出（例如 LLM 的流式生成）。
    
    Args:
        input: 单个输入
        config: 运行配置
        
    Yields:
        输出（可能分多次 yield）
    """
    yield self.invoke(input, config, **kwargs)


# 6. astream (异步流式输出)
# ============================================================================
async def astream(
    self,
    input: Input,
    config: RunnableConfig | None = None,
    **kwargs: Any | None,
) -> AsyncIterator[Output]:
    """
    异步流式输出。
    
    默认实现：只调用一次 ainvoke() 并 yield 结果。
    
    子类应该重写此方法以实现真正的异步流式输出。
    """
    yield await self.ainvoke(input, config, **kwargs)


# ============================================================================
# 管道操作符重载
# ============================================================================

def __or__(self, other) -> RunnableSequence:
    """
    使用 | 操作符组合两个 Runnable。
    
    chain = runnable_1 | runnable_2
    
    工作流程:
    1. 将右边的对象转换为 Runnable
    2. 返回 RunnableSequence(self, coerced_other)
    """
    return RunnableSequence(self, coerce_to_runnable(other))


# ============================================================================
# Schema 相关方法
# ============================================================================

@property
def InputType(self) -> type[Input]:
    """
    获取输入类型。
    
    工作流程:
    1. 遍历类的 MRO（Method Resolution Order）查找 __pydantic_generic_metadata__
    2. 如果是 Pydantic 模型，从泛型参数提取输入类型
    3. 否则从 __orig_bases__ 查找泛型参数
    4. 如果都找不到，抛出 TypeError
    """
    pass


@property
def OutputType(self) -> type[Output]:
    """
    获取输出类型。
    
    原理同 InputType，返回泛型的第二个参数。
    """
    pass


@property
def input_schema(self) -> type[BaseModel]:
    """
    获取输入 Pydantic 模型。
    
    用于验证和序列化输入。
    """
    return self.get_input_schema()


@property
def output_schema(self) -> type[BaseModel]:
    """
    获取输出 Pydantic 模型。
    
    用于验证和序列化输出。
    """
    return self.get_output_schema()


# ============================================================================
# 配置方法
# ============================================================================

def with_retry(self, stop_after_attempt: int = 3, **retry_kwargs):
    """
    为 Runnable 添加重试策略。
    
    返回一个新的 Runnable，遇到异常时会自动重试。
    """
    pass


def with_fallbacks(self, fallbacks: list[Runnable]):
    """
    为 Runnable 添加备选方案。
    
    如果主 Runnable 失败，按顺序尝试备选方案。
    """
    pass


def configurable_fields(self, **kwargs):
    """
    标记 Runnable 的某些字段为可配置。
    
    允许在运行时动态改变这些字段的值。
    """
    pass


# ============================================================================
# 关键特性总结
# ============================================================================

"""
Runnable 的核心特性：

1. **执行方法族**:
   - invoke/ainvoke: 单个输入
   - batch/abatch: 多个输入（并行）
   - stream/astream: 流式输出
   - astream_log: 流式输出 + 中间结果日志
   - astream_events: 流式事件

2. **默认实现**:
   - batch: 使用线程池并行执行 invoke()
   - abatch: 使用 asyncio.gather 并行执行 ainvoke()
   - stream: 调用一次 invoke() 然后 yield
   - astream: 调用一次 ainvoke() 然后 yield
   - ainvoke: 使用线程池执行 invoke()
   
3. **组合**:
   - 使用 | 操作符（__or__）链式组合
   - 返回 RunnableSequence
   - 支持嵌套和复杂链

4. **Schema 反射**:
   - InputType/OutputType: 从泛型参数推断
   - input_schema/output_schema: 获取 Pydantic 模型
   - 用于自动文档、验证、IDE 提示

5. **配置系统**:
   - RunnableConfig: 包含 tags、metadata、max_concurrency 等
   - 支持动态配置字段
   - 支持条件逻辑（if-else、fallback 等）
"""
