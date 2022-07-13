from pydantic import BaseSettings


class Settings(BaseSettings):
    airtable_table_name: str
    airtable_base_id: str
    api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
