import os
import subprocess

import json5
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool

llm_cfg = {
    
    # Use your own model service compatible with OpenAI API:
    #'model': 'Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4',
    #'model_server': 'server address',
    #'api_key': '??',
    # It will use the `DASHSCOPE_API_KEY' environment variable if 'api_key' is not set here.

    # Use the model service provided by DashScope:
    'model': 'qwen-max',
    'model_server': 'dashscope',  # api_base
    'api_key': 'sk-??',
    # (Optional) LLM hyperparameters for generation:
    'generate_cfg': {
        'top_p': 0.5,
        'temperature':0,
    },
}
system = '你是一个Linux专家.先分析当前所处系统的环境和架构，然后用中文和我交流，完成我的指令。'


@register_tool('readPermit')
class ReadPermit(BaseTool):
    description = '遍历读取指定目录及其子目录下所有文件和文件夹的权限信息'
    parameters = [{
        'name': 'path',
        'type': 'string',
        'description': '指定目录的绝对路径',
        'required': True
    }]

    def call(self, params: str, **kwargs) -> str:
        path = json5.loads(params)['path']
        # 检查路径是否存在
        if not os.path.isdir(path):
            return f"Error: The path '{path}' is not a valid directory."

        try:
            formatted_output = []
            # 使用 os.walk 遍历目录及其子目录
            for root, dirs, files in os.walk(path):
                # 获取当前目录下的所有条目（文件和文件夹）
                entries = dirs + files
                for entry in entries:
                    full_path = os.path.join(root, entry)
                    # 使用 ls -l 命令获取单个文件或文件夹的权限信息
                    result = subprocess.run(
                        ["ls", "-ld", full_path],       # 执行 ls -ld 命令
                        stdout=subprocess.PIPE,       # 捕获标准输出
                        stderr=subprocess.PIPE,       # 捕获标准错误
                        text=True                     # 输出为字符串格式
                    )

                    # 检查命令是否成功执行
                    if result.returncode != 0:
                        return f"Error: Failed to execute 'ls -ld {full_path}'.\nDetails: {result.stderr}"

                    # 解析输出并提取权限和文件名
                    parts = result.stdout.split()
                    if len(parts) >= 9:  # 确保是有效的文件信息行
                        permissions = parts[0]  # 权限部分
                        filename = parts[-1]    # 文件名部分
                        formatted_output.append(f"{permissions} {filename}")

            # 将结果拼接成字符串，每行一个
            return "\r\n".join(formatted_output)

        except Exception as e:
            return f"Error: An exception occurred.\nDetails: {str(e)}"
        
@register_tool('changePermit')
class ChangePermit(BaseTool):
    description = '修改指定文件的权限信息'
    parameters = [
        {
            'name': 'path',
            'type': 'string',
            'description': '指定文件的绝对路径',
            'required': True
        },
        {
            'name': 'permit',
            'type': 'string',
            'description': '将要使用chmod命令赋予其的权限代码（如 777、640等），格式为3位数字',
            'required': True
        }
    ]

    def call(self, params: str, **kwargs) -> str:
        path = json5.loads(params)['path']
        permit = json5.loads(params)['permit']

        try:
            # 使用 chmod 命令修改文件权限
            result = subprocess.run(
                ["chmod", permit, path],
                stdout=subprocess.PIPE,       # 捕获标准输出
                stderr=subprocess.PIPE,       # 捕获标准错误
                text=True                     # 输出为字符串格式
            )

            # 检查命令是否成功执行
            if result.returncode != 0:
                return f"Error: Failed to execute 'ls -l'.\nDetails: {result.stderr}"
            else:
                return '权限修改成功'

        except Exception as e:
            return f"Error: An exception occurred.\nDetails: {str(e)}"
        

@register_tool('excuteShell')
class ExcuteShell(BaseTool):
    description = '执行Shell命令，不能执行没有输出的命令'
    parameters = [
        {
            'name': 'cmd',
            'type': 'string',
            'description': '要执行的命令',
            'required': True
        },
    ]

    def call(self, params: str, **kwargs) -> str:
        cmd = json5.loads(params)['cmd']

        try:
            # 使用 chmod 命令修改文件权限
            result = subprocess.run(
                cmd,
                shell=True,  
                stdout=subprocess.PIPE,       # 捕获标准输出
                stderr=subprocess.PIPE,       # 捕获标准错误
                text=True                     # 输出为字符串格式
            )

            # 检查命令是否成功执行
            if result.returncode != 0:
                return f"Error: Failed to execute 'ls -l'.\nDetails: {result.stderr}"
            else:
                return result.stdout

        except Exception as e:
            return f"Error: An exception occurred.\nDetails: {str(e)}"


tools = ['readPermit','changePermit','excuteShell']
bot = Assistant(llm=llm_cfg,
                system_message=system,
                function_list=tools,
                #files=[os.path.abspath('doc.pdf')]
                )

messages = []
while True:
    query = input('user question: ')
    if query == "":
        continue
    messages.append({'role': 'user', 'content': query})
    response = []
    for response in bot.run(messages=messages):
        print('bot response:', response)
    print()
    messages.extend(response)
