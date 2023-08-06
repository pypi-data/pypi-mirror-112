import asyncpg  # type: ignore

from .config import CONFIG, DB_RELEVANT


async def init_db_pool(app_name):
    db_url = f"postgres://{CONFIG['DB_USER']}:{CONFIG['DB_PASSWORD']}@{CONFIG['DB_HOST']}/{CONFIG['DB_NAME']}"   # noqa: E501
    db_url_redacted = f"postgres://{CONFIG['DB_USER']}:***@{CONFIG['DB_HOST']}"
    print(f"Connecting to {db_url_redacted}")
    pool = await asyncpg.create_pool(
        dsn=db_url, min_size=CONFIG['MAX_DB_CONNECTIONS'],
        max_size=CONFIG['MAX_DB_CONNECTIONS'])
    async with pool.acquire() as conn:
        for k, v in DB_RELEVANT[app_name].items():
            await conn.execute(
                'INSERT INTO settings (name, value) VALUES ($1,$2) '
                'ON CONFLICT ON CONSTRAINT settings_pkey DO '
                'UPDATE SET value = $2 WHERE settings.name = $1;', k, str(v))
    return pool
