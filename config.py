from pydantic import BaseSettings, Field


class DBSettings(BaseSettings):
    host: str = Field(validation_alias="HOST")
    port: int = Field(validation_alias="PORT")
    user: str = Field(validation_alias="UESR")
    password: str = Field(validation_alias="PASSWORD")
    database: str = Field(validation_alias="DATABASE")

    class Config:
        env_file = ".env"


class TokenSettings(BaseSettings):
    secret_key: str = Field(validation_alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_algorithm: str = Field(validation_alias="JWT_ALGORITHM")

    class Config:
        env_file = ".env"
