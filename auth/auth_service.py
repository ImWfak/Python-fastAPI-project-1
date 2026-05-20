import os

import bcrypt
from dotenv import load_dotenv
from jose import jwt

from auth.auth_schema import TokenPayloadSchema

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]


async def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


async def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)


async def create_access_token(token_payload_schema: TokenPayloadSchema) -> str:
    return jwt.encode(
        claims=token_payload_schema.model_dump(),
        key=SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
