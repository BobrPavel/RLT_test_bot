# --------------------------------------------------------------------------------
# Модуль обработки команд из приватных чатов
# --------------------------------------------------------------------------------
# Импорты
# --------------------------------------------------------------------------------

import json

from aiogram import types, Router
from aiogram.filters import CommandStart, Command

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



# Обработка всех входящих сообщений
@user_private_router.message()
async def request_handler(message: types.Message):
    print(f"Вопрос: {message.text}")
    agent = await init_agent()
    try:
        query_plan_str = await agent.invoke(content=f"{SYSTEM_PROMPT}\n{message.text}")
        query_plan = json.loads(query_plan_str)
        result = await query_tool(query_plan)
    except Exception as e:
        print(f"Ошиюка: {e}")
        result = "0"


    # query_plan_str = await agent.invoke(content=f"{SYSTEM_PROMPT}\n{message.text}")
    # query_plan = json.loads(query_plan_str)
    # result = await query_tool(query_plan)

    print(f"Ответ: {str(result)}")
    await message.answer(str(result))

