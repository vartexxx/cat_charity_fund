from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
