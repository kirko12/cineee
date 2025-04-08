import os
import traceback
from werkzeug.exceptions import HTTPException
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from dotenv import load_dotenv
from config import Config

# Cargar el archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Agregar funciones para imprimir mensajes de depuración
@app.before_first_request
def before_first_request():
    print("Inicializando la app...")

@app.after_request
def after_request(response):
    print(f"Solicitud procesada con status {response.status}")
    return response

# Cargar el usuario actual
@login_manager.user_loader
def load_user(user_id):
    from models import Usuario
    return Usuario.query.get(int(user_id))

# Importar rutas
from routes import *

# Función para enviar correo en caso de error grave
def send_error_email(error_trace):
    msg = Message(
        subject="Error en la aplicación Flask",
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[app.config['MAIL_USERNAME']],
        body=f"Se ha producido un error en la aplicación:\n\n{error_trace}"
    )
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Manejador global de errores
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException) and e.code < 500:
        return render_template("error.html", error=e), e.code

    error_trace = traceback.format_exc()
    send_error_email(error_trace)
    return render_template("error.html", error=e), 500

# Probar la conexión a la base de datos
with app.app_context():
    try:
        db.create_all()
        print("Conexión a la base de datos exitosa.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")




