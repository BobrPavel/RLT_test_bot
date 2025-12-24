# --------------------------------------------------------------------------------
# Модуль обработки команд из приватных чатов
# --------------------------------------------------------------------------------
# Импорты
# --------------------------------------------------------------------------------

import json

from aiogram import types, Router
from aiogram.filters import CommandStart

from common.prompts import SYSTEM_PROMPT
from llm.agent_init import init_agent
from llm.agent_tools import query_tool

# --------------------------------------------------------------------------------
# Настройки и константы
# --------------------------------------------------------------------------------


user_private_router = Router()


# --------------------------------------------------------------------------------
# Обработчики
# --------------------------------------------------------------------------------



# Стартовая команда
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Для работы с ботом введите вопрос на естественном русском языке")


@user_private_router.message()
async def request_handler(message: types.Message):
    agent = await init_agent()

    query_plan_str = await agent.invoke(content=f"{SYSTEM_PROMPT}\n{message.text}")
    
    query_plan = json.loads(query_plan_str)
    result = await query_tool(query_plan)
    
    await message.answer(str(result))

