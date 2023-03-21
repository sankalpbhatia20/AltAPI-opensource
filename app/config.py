from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    huggingface_token: str 

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()