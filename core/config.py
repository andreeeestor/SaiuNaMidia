from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AUTH_USER: str = "admin"
    AUTH_PASSWORD: str = "admin"
    JWT_SECRET: str = "saiunamidia_secret_key_2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
