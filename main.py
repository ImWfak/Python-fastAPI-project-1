from fastapi import FastAPI

from db.connect_to_db import connect_to_db
from product.product_router import product_router

app = FastAPI()

app.include_router(product_router)

connect_to_db(app)
