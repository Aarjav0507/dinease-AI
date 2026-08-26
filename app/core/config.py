from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Configuration
    """

    # ----------------------------
    # Application
    # ----------------------------
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    # ----------------------------
    # Server
    # ----------------------------
    HOST: str
    PORT: int

    # ----------------------------
    # Database
    # ----------------------------
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # ----------------------------
    # JWT
    # ----------------------------
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    
     # Razorpay
     # ----------------------------
    RAZORPAY_KEY_ID: str
    RAZORPAY_KEY_SECRET: str

     #email sender
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    
    EMAIL_FROM: str

    # mistral AI
    MISTRAL_API_KEY: str

    # ----------------------------
    # Read .env file
    # ----------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
   


settings = Settings()

