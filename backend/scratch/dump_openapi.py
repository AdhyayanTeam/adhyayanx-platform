import asyncio
from httpx import AsyncClient
from app.api.main import app

import httpx

async def main():
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/openapi.json")
        data = res.json()
        paths = list(data["paths"].keys())
        for p in paths:
            if "delivery" in p:
                print(p)

if __name__ == "__main__":
    asyncio.run(main())
