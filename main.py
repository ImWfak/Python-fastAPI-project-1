from fastapi import FastAPI

from db.connect_to_db import connect_to_db
from exception.app_exception import AppException
from product.product_router import product_router
from exception.app_exception_handler import app_exception_handler

app = FastAPI()

app.add_exception_handler(AppException, app_exception_handler)
app.include_router(product_router)

connect_to_db(app)
