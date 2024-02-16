class Settings:

    DATABASE_URL: str = "sqlite:///./db.sqlite"
    SECRET_KEY: str = "something here (recommend: openssl rand -hex 32)"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 2880
    UPLOADS_PATH: str = "uploads"
    DEFAULT_PASS: str = "default"
    ALLOWED_EXTENSIONS: list[str] = [".png", ".jpg", ".jpeg", ".gif"]
    ORIGINS: list[str] = [
        "http://localhost:3000",
    ]


def get_settings():
    return Settings()


settings = get_settings()
