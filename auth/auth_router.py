from fastapi import APIRouter
from starlette import status

from auth.auth_schema import SingInSchema, SignUpSchema
from auth.auth_service import sign_up_service, sign_in_service

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post("/sign-in")
async def sing_in(sign_in_schema: SingInSchema) -> str:
    return await sign_in_service(sign_in_schema)


@auth_router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up_router(sing_up_schema: SignUpSchema) -> str:
    return await sign_up_service(sing_up_schema)
