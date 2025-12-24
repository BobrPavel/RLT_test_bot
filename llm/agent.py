# --------------------------------------------------------------------------------
# Агент
# --------------------------------------------------------------------------------
# Импорты
# --------------------------------------------------------------------------------

import uuid

from typing import Sequence

from langchain_core.language_models import LanguageModelLike
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver


# --------------------------------------------------------------------------------
# Код агента
# --------------------------------------------------------------------------------



class LLMAgent:
    def __init__(self, model: LanguageModelLike, tools: Sequence[BaseTool]):
        self._model = model
        self._tools = tools
        self._config: RunnableConfig = {
                "configurable": {"thread_id": uuid.uuid4().hex}}
        self._agent = None


    async def ainit(self): 
        """Асинхронная инициализация агента"""
        self._agent = create_react_agent(
            self._model,
            tools=[],
            checkpointer=MemorySaver()
        )
        return self


    async def invoke(
        self,
        content: str,
        temperature: float=0.1
    ) -> str:
        """Отправляет сообщение в чат"""
        message: dict = {
            "role": "user",
            "content": content,
        }

        response = self._agent.invoke(
            input = {
                "messages": [message],
                "temperature": temperature,
            },
            config=self._config
        )
        return response["messages"][-1].content