from pathlib import Path

import aiofiles
import orjson

from .backends import sql_backend
from .settings import settings


async def get_sql_from_file(name: str) -> str:
    sql_path = Path(settings.sql_dir) / f"{name}.sql"
    async with aiofiles.open(sql_path, mode="r") as sql_file:
        return await sql_file.read()


async def migrate(conn, filename):
    conn = await sql_backend.conn
    sql = await get_sql_from_file(filename)
    await conn.execute(sql)


def orjson_dumps(v, *_, **__):
    return orjson.dumps(v).decode()
