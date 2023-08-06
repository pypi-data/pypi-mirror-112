import asyncpg


class SQLBackend:
    _conn = None
    _pool = None

    @property
    async def conn(self):
        """Return new or current db connection.

        Use standard PG environment variables to establish the connection
        (ex.: PGHOST, PGPORT, etc.).

        Returns:
            asyncpg.connection.Connection
        """
        if not self._conn:
            self._conn = await asyncpg.connect()
        return self._conn

    @property
    async def pool(self):
        """Return new or current pool of connections.

        Use standard PG environment variables to establish the connection
        (ex.: PGHOST, PGPORT, etc.).

        Returns:
            asyncpg.pool.Pool
        """
        if not self._pool:
            self._pool = await asyncpg.create_pool()
        return self._pool


sql_backend = SQLBackend()
