import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from config import Config



# 1. 明确指定语言模型
llm = ChatOpenAI(
    temperature=Config.TEMPERATURE,
    model=Config.OPENAI_MODEL,
    openai_api_key=Config.OPENAI_API_KEY,
    base_url=Config.OPENAI_BASE_URL
)
# 2. 定义专注且目标明确的智能体
planner_writer_agent = Agent(
    role='文章规划与写作专家',
    goal='规划并撰写指定主题的简明、吸引人的摘要。',
    backstory=(
        '你是一名资深技术写手和内容策略师。'
        '你的优势在于写作前先制定清晰可执行的计划，'
        '确保最终摘要既信息丰富又易于理解。'
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm  # 绑定指定 LLM
)

# 3. 定义结构化且具体的任务
topic = "强化学习在 AI 中的重要性"
high_level_task = Task(
    description=(
        f"1. 针对主题'{topic}'制定摘要的要点计划（项目符号列表）。\\n"
        f"2. 根据计划撰写约 200 字的摘要。"
    ),
    expected_output=(
        "最终报告包含两个部分：\\n\\n"
        "### 计划\\n"
        "- 摘要主要观点的项目符号列表。\\n\\n"
        "### 摘要\\n"
        "- 主题的简明、结构化总结。"
    ),
    agent=planner_writer_agent,
)

# 创建 Crew，指定顺序处理流程
crew = Crew(
    agents=[planner_writer_agent],
    tasks=[high_level_task],
    process=Process.sequential,
)

# 执行任务
print("## 正在运行规划与写作任务 ##")
result = crew.kickoff()

print("\\n\\n---\\n## 任务结果 ##\\n---")
print(result)