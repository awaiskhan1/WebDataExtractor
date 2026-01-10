from aiosqlite import connect
from typing import AsyncGenerator

DATABASE_URL = "sqlite:///./webdataextractor.db"

async def get_db_session() -> AsyncGenerator:
    async with connect(DATABASE_URL) as db:
        yield db