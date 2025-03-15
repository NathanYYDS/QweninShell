# QweninShell
Qwen大模型接管系统，执行全自动化操作，解放双手

# 开始上手

## 安装

- 从 PyPI 安装稳定版本：
```bash
pip install -U "qwen-agent[rag,code_interpreter,python_executor,gui]"
# 或者，使用 `pip install -U qwen-agent` 来安装最小依赖。
# 可使用双括号指定如下的可选依赖：
#   [gui] 用于提供基于 Gradio 的 GUI 支持；
#   [rag] 用于支持 RAG；
#   [code_interpreter] 用于提供代码解释器相关支持；
#   [python_executor] 用于支持 Qwen2.5-Math 基于工具的推理。
```

- 或者，你可以从源码安装最新的开发版本：
```bash
git clone https://github.com/QwenLM/Qwen-Agent.git
cd Qwen-Agent
pip install -e ./"[rag,code_interpreter,python_executor]"
# 或者，使用 `pip install -e ./` 安装最小依赖。
```

如果需要内置 GUI 支持，请选择性地安装可选依赖：
```bash
pip install -U "qwen-agent[gui,rag,code_interpreter]"
# 或者通过源码安装 `pip install -e ./"[gui,rag,code_interpreter]"`
```

## 准备：模型服务

Qwen-Agent支持接入阿里云[DashScope](https://help.aliyun.com/zh/dashscope/developer-reference/quick-start)服务提供的Qwen模型服务，也支持通过OpenAI API方式接入开源的Qwen模型服务。

- 如果希望接入DashScope提供的模型服务，只需配置相应的环境变量`DASHSCOPE_API_KEY`为您的DashScope API Key。

- 或者，如果您希望部署并使用您自己的模型服务，请按照Qwen2的README中提供的指导进行操作，以部署一个兼容OpenAI接口协议的API服务。
具体来说，请参阅[vLLM](https://github.com/QwenLM/Qwen2?tab=readme-ov-file#vllm)一节了解高并发的GPU部署方式，或者查看[Ollama](https://github.com/QwenLM/Qwen2?tab=readme-ov-file#ollama)一节了解本地CPU（+GPU）部署。

## 运行
- 如果接入vllm的api接口，请运行run_vllm.py （此版本对vllm的流式输出进行了适配）
- 其他接口运行run.py
