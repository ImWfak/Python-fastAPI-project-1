import os
import pytest
import pytest_asyncio
from tortoise import Tortoise
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport

from main import app
from product.product_model import ProductModel

load_dotenv(".test.env")

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


@pytest_asyncio.fixture(scope="session", autouse=True)
async def connect_test_db():
    await Tortoise.close_connections()

    await Tortoise.init({
        "connections": {
            "default": f"postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        },
        "apps": {
            "models": {
                "models": [
                    "product.product_model"
                ],
                "default_connection": "default"
            }
        }
    })
    await Tortoise.generate_schemas(safe=True)

    yield

    connection = Tortoise.get_connection("default")
    await connection.execute_script("DROP SCHEMA public CASCADE;")
    await connection.execute_script("CREATE SCHEMA public;")

    await Tortoise.close_connections()


@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    await ProductModel.all().delete()
    yield
    await ProductModel.all().delete()


"""@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as async_client:
        yield async_client"""
