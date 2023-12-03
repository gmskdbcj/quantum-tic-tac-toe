import aiosqlite
import asyncio

class Room:
    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = asyncio.Lock()

    async def __aenter__(self):
        self.db = await aiosqlite.connect(self.db_file)
        await self.db.execute("CREATE TABLE IF NOT EXISTS Rooms (player_1 INT PRIMARY KEY , player_2 INT)")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()

    async def find(self):
        async with self.lock:
            async with self.db.execute("SELECT player_1, player_2 FROM Rooms WHERE player_2 = ?", (0,)) as cursor:
                return await cursor.fetchone()

    async def create(self, player_id):
        async with self.lock:
            await self.db.execute("INSERT INTO Rooms (player_1, player_2) VALUES (?, ?)", (player_id, 0))
            await self.db.commit()

    async def delete(self, player_id):
        async with self.lock:
            await self.db.execute("DELETE FROM Rooms WHERE player_1 = ?", (player_id,))
            await self.db.commit()

    async def join(self, my_id, id):
        async with self.lock:
            await self.db.execute("UPDATE Rooms SET player_2 = ? WHERE player_1 = ?", (my_id, id))
            await self.db.commit()
