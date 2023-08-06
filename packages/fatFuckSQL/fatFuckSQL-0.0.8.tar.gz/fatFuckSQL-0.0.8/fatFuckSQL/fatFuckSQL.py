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
            if args: # stupid asyncpg
                return await con.fetch(query, *args)
            else:
                return await con.fetch(query)

    async def fetchval(self, query: str, *args):
        async with self._pool.acquire() as con:
            if args: # stupid asyncpg
                return await con.fetchval(query, *args)
            else:
                return await con.fetchval(query)

    async def fetchrow(self, query: str, *args):
        async with self._pool.acquire() as con:
            if args: # stupid asyncpg
                return await con.fetchrow(query, *args)
            else:
                return await con.fetchrow(query)

    async def execute(self, query: str, *args):
        async with self._pool.acquire() as con:
            if args: # stupid asyncpg
                return await con.execute(query, *args)
            else:
                return await con.execute(query)
            
    async def iter(self, query: str, *args): # fetch() but iteration
        async with self._pool.acquire() as con:
            if args: # stupid asyncpg
                rows = await con.fetch(query, *args)
            else:
                rows = await con.fetch(query)
            
            for row in rows:
                yield row

    async def close(self):
        await self._pool.close()