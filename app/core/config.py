from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    MONGODB_URI : str
    atlas_username : str
    atlas_password : str
    JWT_SECRET: str


settings = Settings()