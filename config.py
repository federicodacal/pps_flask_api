import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://default:rpvCVZO3nyU0@ep-polished-river-a4nq13ut.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # or another method to set a secret key
    MONGO_URI = 'mongodb+srv://federicodacal:s0AzgXnMhMeNM6AN@audiolibredb.agzzv.mongodb.net/audiolibredb'

    # Configuración SMTP
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    smtp_port_str = os.getenv("SMTP_PORT")
    if smtp_port_str is not None and smtp_port_str.isdigit():
        SMTP_PORT = int(smtp_port_str)