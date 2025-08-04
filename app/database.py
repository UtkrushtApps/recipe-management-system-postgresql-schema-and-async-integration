import asyncpg
from typing import Any

DB_CONFIG = {
    'database': 'recipes',
    'user': 'utkrusht',
    'password': 'utkrushtpass',
    'host': 'postgres',
    'port': 5432,
}

async def get_db_pool() -> Any:
    return await asyncpg.create_pool(**DB_CONFIG)
