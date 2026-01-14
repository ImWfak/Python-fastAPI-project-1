from fastapi import FastAPI

from db.connect_to_db import connect_to_db

app = FastAPI()

connect_to_db(app)
