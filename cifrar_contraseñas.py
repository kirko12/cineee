from werkzeug.security import generate_password_hash
from app import app, db
from models import Usuario

# Crear un contexto de aplicación
with app.app_context():
    # Buscar al usuario con la contraseña en texto claro (aquí se usa id=1 como ejemplo)
    usuario = Usuario.query.get(1)  # Cambia este ID según el usuario que quieras actualizar

    # Verificar si el usuario existe
    if usuario:
        # Cifrar la contraseña utilizando pbkdf2:sha256
        usuario.password = generate_password_hash('admin123', method='pbkdf2:sha256')

        # Guardar el cambio en la base de datos
        db.session.commit()

        print(f"Contraseña cifrada para el usuario {usuario.nombre} y actualizada correctamente.")
    else:
        print("El usuario no existe.")
