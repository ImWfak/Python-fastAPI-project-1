import os

import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise

from main import app

load_dotenv(".test.env")

HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
DATABASE = os.environ["DATABASE"]


@pytest_asyncio.fixture(scope="function", autouse=True)
async def db():
    await Tortoise.init({
        "connections": {
            "default": f"postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        },
        "apps": {
            "models": {
                "models": [
                    "product.product_model",
                    "user.user_model"
                ],
                "default_connection": "default"
            }
        }
    })
    await Tortoise.generate_schemas(safe=True)

    yield

    try:
        await Tortoise.get_connection("default").execute_script(
            """
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;
            """
        )

    finally:
        await Tortoise.close_connections()


@pytest_asyncio.fixture()
async def async_client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8080"
    ) as async_client:
        yield async_client
