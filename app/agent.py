from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from app.models.gemini_llm import GeminiLLM
from app.tools.web_search import duckduckgo_search


def build_agent(verbose: bool = False):
    # LLM wrapper
    llm = GeminiLLM(temperature=0.0)

    # Tools
    tools = [
        Tool(
            name="WebSearch",
            func=duckduckgo_search,
            description="Search the web for factual information using DuckDuckGo.",
        )
    ]

    # Memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Prompt Template
    template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Previous conversation history:
{chat_history}

Question: {input}
Thought:{agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)

    # Create agent
    agent = create_react_agent(llm, tools, prompt)

    # Create executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=verbose,
        handle_parsing_errors=True
    )

    return agent_executor
