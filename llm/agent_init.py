# --------------------------------------------------------------------------------
# Инициализация агента
# --------------------------------------------------------------------------------
# Импорты
# --------------------------------------------------------------------------------

from langchain_gigachat.chat_models import GigaChat
from llm.agent import LLMAgent  

# --------------------------------------------------------------------------------
# Код инициализации
# --------------------------------------------------------------------------------

agent: LLMAgent | None = None

async def init_agent() -> LLMAgent:
    global agent
    if agent is not None:
        return agent

    model = GigaChat(model="GigaChat-2-Max", verify_ssl_certs=False,)  # создаём модель   

    agent = await LLMAgent(model, tools=[]).ainit() # создаём асинхронного агента через ainit()

    return agent


