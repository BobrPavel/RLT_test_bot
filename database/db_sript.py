import asyncio
import asyncpg

DB_NAME = "RLT_test_bot"
DB_USER = "RLT_test_bot"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = 5432


async def create_database():
    # Подключаемся к системной БД postgres
    conn = await asyncpg.connect(
        user="postgres",
        password="1234",
        database="postgres",
        host=DB_HOST,
        port=DB_PORT
    )

    # Проверяем, существует ли база
    exists = await conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname = $1", DB_NAME
    )

    if not exists:
        await conn.execute(f'CREATE DATABASE "{DB_NAME}"')
        print(f"БД {DB_NAME} создана")
    else:
        print(f"БД {DB_NAME} уже существует")

    await conn.close()

if __name__ == "__main__":
    asyncio.run(create_database())
