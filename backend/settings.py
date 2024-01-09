class Settings:

    DATABASE_URL: str = "sqlite:///./db.sqlite"
    SECRET_KEY: str = "something here (recommend: openssl rand -hex 32)"
    ALGORITHM: str = "HS256"
    ORIGINS: list[str] = [
        "http://localhost:3000",
    ]


def get_settings():
    return Settings()


settings = get_settings()
