from app import db  # Aquí importamos db que ya está inicializado en app.py

class Pelicula(db.Model):
    __tablename__ = 'peliculas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    trailer_url = db.Column(db.String(255))
    sala = db.Column(db.String(50), nullable=False)  # 👈 Nuevo campo

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)  # Agrega esta línea
    
    def get_id(self):
        return str(self.id)  # Devuelve el ID como string

    def is_authenticated(self):
        return True  # Esto siempre devuelve True si el usuario está autenticado

    def is_active(self):
        return self.is_active  # Devuelve si la cuenta está activa, puedes personalizarlo según tu lógica

    def is_anonymous(self):
        return False  # Siempre devuelve False si el usuario está autenticado