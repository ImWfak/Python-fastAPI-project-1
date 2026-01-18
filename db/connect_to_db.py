import os
from fastapi import FastAPI
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


def connect_to_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=f"postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
        modules={
            "models": [
                "product.product_model"
            ]
        },
        generate_schemas=True,
        add_exception_handlers=True
    )
