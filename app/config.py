from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database: str = "postgresql+psycopg"
    database_user: str = "postgres"
    database_password: str
    database_host: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"

settings = Settings()