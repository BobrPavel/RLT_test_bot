from langchain_gigachat.chat_models import GigaChat
from llm.agent import LLMAgent  # твой асинхронный агент
from llm.agent_tools import query_tool

agent: LLMAgent | None = None

async def init_agent() -> LLMAgent:
    global agent
    if agent is not None:
        return agent

    # создаём модель
    model = GigaChat(
        model="GigaChat-2-Max",
        verify_ssl_certs=False,
    )

    # создаём асинхронного агента через ainit()
    agent = await LLMAgent(model, tools=[]).ainit()

    return agent

