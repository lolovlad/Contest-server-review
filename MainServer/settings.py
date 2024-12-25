from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_host: str
    server_port: int
    static_path: str

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_db: str
    postgres_password: str
    pgport: int

    redis_password: str
    redis_user: str
    redis_user_password: str

    redis_host: str
    redis_port: int

    minio_access_key: str
    minio_secret_key: str
    minio_default_buckets: str
    minio_host: str
    minio_port: str

    minio_root_user: str
    minio_root_password: str

    websocket_server_host: str
    websocket_server_port: int



settings = Settings(_env_file="settings_server_debug.env", _env_file_encoding="utf-8")
