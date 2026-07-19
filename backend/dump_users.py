import asyncio
import os
from sqlalchemy import text
from app.infrastructure.postgres.database import Database
from app.kernel.config.loader import Settings

async def main():
    settings = Settings()
    db = Database(settings.database_url)
    async with db.session() as session:
        result = await session.execute(text("SELECT id, email, is_active FROM users"))
        rows = result.fetchall()
        print("Users in DB:")
        for row in rows:
            print(row)

if __name__ == "__main__":
    asyncio.run(main())
