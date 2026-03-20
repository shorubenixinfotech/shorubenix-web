import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://uh68ejdcgxzosjxmzxl6:2DOjUOj9P5FSuhAeoQYub8qrxZajCq@bditexumkeggwqxmthvw-postgresql.services.clever-cloud.com:50013/bditexumkeggwqxmthvw"

    # Server
    PORT: int = 3001
    NODE_ENV: str = "development"

    # JWT
    JWT_SECRET: str = "shorubenix_jwt_secret_key_2024_secure"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Razorpay
    RAZORPAY_KEY_ID: str = "rzp_live_SSKuly2gksJCuu"
    RAZORPAY_KEY_SECRET: str = "dfq1J437AyIG3TjzvXfA15A5"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
