import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    SES_SMTP_HOST = os.getenv("SES_SMTP_HOST")
    SES_SMTP_PORT = int(os.getenv("SES_SMTP_PORT", 587))
    SES_SMTP_USER = os.getenv("SES_SMTP_USER")
    SES_SMTP_PASS = os.getenv("SES_SMTP_PASS")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")