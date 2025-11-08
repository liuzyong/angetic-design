# Copyright (c) 2025 Marco Fago
#
# 本代码采用 MIT 许可证，详见仓库 LICENSE 文件。

import uuid
from typing import Dict, Any, Optional

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool
from google.genai import types
from google.adk.events import Event

# --- 定义工具函数 ---
def booking_handler(request: str) -> str:
    """
    处理机票和酒店预订请求。
    Args:
        request: 用户的预订请求。
    Returns:
        预订处理确认信息。
    """
    print("-------------------------- 预订处理器已调用 ----------------------------")
    return f"已模拟处理预订请求：'{request}'。"

def info_handler(request: str) -> str:
    """
    处理一般信息请求。
    Args:
        request: 用户问题。
    Returns:
        信息检索处理结果。
    """
    print("-------------------------- 信息处理器已调用 ----------------------------")
    return f"信息请求：'{request}'。结果：模拟信息检索。"

def unclear_handler(request: str) -> str:
    """处理无法委托的请求。"""
    return f"协调者无法委托请求：'{request}'。请补充说明。"

# --- 创建工具 ---
booking_tool = FunctionTool(booking_handler)
info_tool = FunctionTool(info_handler)

# 定义配备工具的专用子智能体
booking_agent = Agent(
    name="Booker",
    model="gemini-2.0-flash",
    description="专门处理机票和酒店预订请求，通过 booking tool 实现。",
    tools=[booking_tool]
)

info_agent = Agent(
    name="Info",
    model="gemini-2.0-flash",
    description="专门提供一般信息和答疑，通过 info tool 实现。",
    tools=[info_tool]
)

# 定义父智能体（协调者），包含委托指令
coordinator = Agent(
    name="Coordinator",
    model="gemini-2.0-flash",
    instruction=(
        "你是主协调者，只负责分析用户请求并委托给合适的专用智能体。"
        "不要直接回答用户。\n"
        "- 任何涉及机票或酒店预订的请求，委托给 'Booker' 智能体。\n"
        "- 其他一般信息问题，委托给 'Info' 智能体。"
    ),
    description="负责将用户请求路由到正确专用智能体的协调者。",
    sub_agents=[booking_agent, info_agent]
)

# --- 执行逻辑 ---

async def run_coordinator(runner: InMemoryRunner, request: str):
    """用给定请求运行协调者智能体并委托。"""
    print(f"\n--- 协调者运行请求：'{request}' ---")
    final_result = ""
    try:
        user_id = "user_123"
        session_id = str(uuid.uuid4())
        await runner.session_service.create_session(
            app_name=runner.app_name, user_id=user_id, session_id=session_id
        )

        for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(
                role='user',
                parts=[types.Part(text=request)]
            ),
        ):
            if event.is_final_response() and event.content:
                if hasattr(event.content, 'text') and event.content.text:
                    final_result = event.content.text
                elif event.content.parts:
                    text_parts = [part.text for part in event.content.parts if part.text]
                    final_result = "".join(text_parts)
                break

        print(f"协调者最终响应：{final_result}")
        return final_result
    except Exception as e:
        print(f"处理请求时发生错误：{e}")
        return f"处理请求时发生错误：{e}"

async def main():
    """主函数，运行 ADK 示例。"""
    print("--- Google ADK 路由示例（ADK Auto-Flow 风格）---")
    print("注意：需安装并认证 Google ADK。")

    runner = InMemoryRunner(coordinator)
    # 示例用法
    result_a = await run_coordinator(runner, "帮我预订巴黎的酒店。")
    print(f"最终输出 A: {result_a}")
    result_b = await run_coordinator(runner, "世界最高的山峰是什么？")
    print(f"最终输出 B: {result_b}")
    result_c = await run_coordinator(runner, "说一个随机的事实。")  # 应委托给 Info
    print(f"最终输出 C: {result_c}")
    result_d = await run_coordinator(runner, "查找下个月飞往东京的航班。")  # 应委托给 Booker
    print(f"最终输出 D: {result_d}")

if __name__ == "__main__":
    import nest_asyncio
    import asyncio
    nest_asyncio.apply()
    asyncio.run(main())