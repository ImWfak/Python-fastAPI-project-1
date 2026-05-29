from pydantic import BaseSettings, Field


class DBSettings(BaseSettings):
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")
    user: str = Field(alias="UESR")
    password: str = Field(alias="PASSWORD")
    database: str = Field(alias="DATABASE")

    class Config:
        env_file = ".env"


class TokenSettings(BaseSettings):
    secret_key: str = Field(alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_algorithm: str = Field(alias="JWT_ALGORITHM")

    class Config:
        env_file = ".env"
