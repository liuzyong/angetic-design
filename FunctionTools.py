import os
import getpass
import asyncio
import nest_asyncio
from typing import List
from dotenv import load_dotenv
import logging

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool as langchain_tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from config import Config


# 安全输入 API 密钥并设置为环境变量（注释掉避免阻塞）
# os.environ["GOOGLE_API_KEY"] = getpass.getpass("输入你的 Google API 密钥：")
# os.environ["OPENAI_API_KEY"] = getpass.getpass("输入你的 OpenAI API 密钥：")

# 初始化语言模型（推荐使用 ChatOpenAI）
llm = ChatOpenAI(
    temperature=Config.TEMPERATURE,
    model=Config.OPENAI_MODEL,
    openai_api_key=Config.OPENAI_API_KEY,
    base_url=Config.OPENAI_BASE_URL
)


# --- 定义工具 ---
@langchain_tool
def search_information(query: str) -> str:
    """
    根据主题提供事实信息。用于回答如"法国首都"或"伦敦天气？"等问题。
    """
    print(f"\n--- 🛠️ ✅ 工具调用：search_information, 查询：'{query}' ---")
    # 用预设结果模拟搜索工具
    simulated_results = {
        "weather in london": "伦敦当前天气多云，气温 15°C。",
        "法国的首都": "法国的首都是巴黎。",
        "population of earth": "地球人口约 80 亿。",
        "tallest mountain": "珠穆朗玛峰是海拔最高的山峰。",
        "default": f"模拟搜索 '{query}'：未找到具体信息，但该主题很有趣。"
    }

    result = simulated_results.get(query.lower(), simulated_results["default"])
    print(f"--- 工具结果：{result} ---")
    return result

tools = [search_information]

# --- 创建工具调用 Agent ---
if llm:
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个乐于助人的助手。"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, agent_prompt)
    agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)

    async def run_agent_with_tool(query: str):
        """用 Agent 执行查询并打印最终回复。"""
        print(f"\n--- 🤖 Agent 运行查询：'{query}' ---")
        try:
            response = await agent_executor.ainvoke({"input": query})
            print("\n--- ✅ Agent 最终回复 ---")
            print(response["output"])
        except Exception as e:
            print(f"\n❌ Agent 执行出错：{e}")

    async def main():
        """并发运行多个 Agent 查询。"""
        tasks = [
            run_agent_with_tool("法国的首都是什么？"),
            # run_agent_with_tool("伦敦天气如何？"),
            # run_agent_with_tool("说说狗的相关信息。")  # 触发默认工具回复
        ]
        await asyncio.gather(*tasks)

    nest_asyncio.apply()
    asyncio.run(main())