from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str
    server_port: int
    database_name: str
    static_path: str


settings = Settings(_env_file="settings_server.env", _env_file_encoding="utf-8")
