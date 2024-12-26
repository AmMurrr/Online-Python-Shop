from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Config
    db_username: str
    db_password: str
    db_hostname: str
    db_port: str
    db_name: str

    class Config:
        env_file = "env.env"


settings = Settings()

# print(settings)
