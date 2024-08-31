import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://default:rpvCVZO3nyU0@ep-polished-river-a4nq13ut-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # or another method to set a secret key