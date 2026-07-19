import asyncio
from fastapi import FastAPI
from app.api.main import app

def dump_routes():
    for route in app.routes:
        print(getattr(route, "path", type(route).__name__))

if __name__ == "__main__":
    dump_routes()
