import os
import cloudinary
from dotenv import load_dotenv
from urllib.parse import quote

# Cargar variables del entorno
load_dotenv()

# 🔍 Debug opcional
print("CLOUDINARY CONFIG:")
print("CLOUD_NAME:", os.getenv('CLOUDINARY_CLOUD_NAME'))
print("API_KEY:", os.getenv('CLOUDINARY_API_KEY'))

# ✅ Configurar Cloudinary al cargar el archivo
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

class Config:
    username = quote(os.getenv('MYSQLUSER'))
    password = quote(os.getenv('MYSQLPASSWORD'))
    host = os.getenv('MYSQLHOST')
    port = os.getenv('MYSQLPORT')
    database = os.getenv('MYSQLDATABASE')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
