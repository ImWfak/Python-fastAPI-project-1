import os
import pytest_asyncio
from tortoise import Tortoise
from dotenv import load_dotenv

load_dotenv(".test.env")

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def db():
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

    await Tortoise.get_connection("default").execute_script(
        """
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        """
    )
    await Tortoise.close_connections()
