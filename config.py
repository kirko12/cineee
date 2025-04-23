import os
import cloudinary
from dotenv import load_dotenv
from urllib.parse import quote

# Cargar las variables desde el archivo .env
load_dotenv()

# Depurar antes de asignar a la clase
print("Cargando configuración de base de datos:")
print("HOST:", os.getenv('MYSQLHOST'))
print("PORT:", os.getenv('MYSQLPORT'))
print("USER:", os.getenv('MYSQLUSER'))
print("PASS:", os.getenv('MYSQLPASSWORD'))
print("DB:", os.getenv('MYSQLDATABASE'))

class Config:
    username = quote(os.getenv('MYSQLUSER'))
    password = quote(os.getenv('MYSQLPASSWORD'))
    host = os.getenv('MYSQLHOST')
    port = os.getenv('MYSQLPORT')
    database = os.getenv('MYSQLDATABASE')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

    # Seguridad y media
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
      # Cloudinary config
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Debug controlado por variable de entorno
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'

    cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)