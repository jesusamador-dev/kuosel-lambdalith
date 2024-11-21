import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # Configuración de AWS Cognito
    COGNITO_USER_POOL_ID: str = Field(..., env="COGNITO_USER_POOL_ID")
    COGNITO_CLIENT_ID: str = Field(..., env="COGNITO_CLIENT_ID")
    AWS_REGION: str = os.getenv("AWS_REGION")
    COGNITO_DOMAIN: str = Field(..., env="COGNITO_DOMAIN")
    COGNITO_CLIENT_SECRET: str = Field(..., env="COGNITO_CLIENT_SECRET")

    # Configuración de la base de datos PostgreSQL
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(..., env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")

    class Config:
        # Esto le indica a Pydantic que debe buscar las variables en el entorno de Lambda
        case_sensitive = True


# Crea una instancia de Settings, que tomará automáticamente los valores de las variables de entorno
settings = Settings()
