from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    pghost: str
    pgport: str
    pgpassword: str
    pgdatabase: str
    pguser: str
    huggingface_token: str 
    finnhub_token: str
    openai_token: str

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()