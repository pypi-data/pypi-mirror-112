import asyncio
import asyncpg # troll

class fatFuckSQL:
    def __init__(self): # blank init vars
        self._loop = None # _var because internal xd
        self._pool = None

    @classmethod
    async def connect(self, db: str, host: str, password: str, user: str, loop = None):
        self = self()
        
        self._loop = loop or asyncio.get_event_loop()
        
        self._pool = await asyncpg.create_pool(
            user=user,
            password=password,
            database=db,
            host=host
        )
        
        return self
    
    async def fetch(self, query: str, *args):
        async with self._pool.acquire() as con:
            return await con.fetch(query, args)

    async def fetchval(self, query: str, *args):
        async with self._pool.acquire() as con:
            return await con.fetchval(query, args)

    async def fetchrow(self, query: str, *args):
        async with self._pool.acquire() as con:
            return await con.fetch(query, args)

    async def execute(self, query: str, *args):
        async with self._pool.acquire() as con:
            return await con.execute(query, args)
        
    async def close(self):
        await self._pool.close()