import json

# from langchain_core.tools import tool
# from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import session_maker
from database.orm_query import execute_query




async def query_tool(query_plan_input: dict) -> str:
    """
    Асинхронный инструмент, который получает QueryPlan (JSON строку или dict)
    и возвращает одно число.
    """

    print("tool")
    query_plan = query_plan_input["query_plan"]

    # Создаём сессию внутри инструмента
    async with session_maker() as session:
        result = await execute_query(query_plan, session)

    print(str(result))
    return str(result)
