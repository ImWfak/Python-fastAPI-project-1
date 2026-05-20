import os
from fastapi import FastAPI
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise

load_dotenv()

HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
DATABASE = os.environ["DATABASE"]


def connect_to_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=f"postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
        modules={
            "models": [
                "product.product_model",
                "user.user_model"
            ]
        },
        generate_schemas=True,
        add_exception_handlers=True
    )
