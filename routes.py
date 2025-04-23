import cloudinary
import cloudinary.uploader
from flask import current_app, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from models import Pelicula, Usuario
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import os
from config import Config


# Ruta principal (Cartelera)
@app.route('/', methods=['GET', 'POST'])
def home():
    # Obtener los parámetros de búsqueda
    fecha = request.args.get('fecha')
    genero = request.args.get('genero')

    # Filtrar las películas según los parámetros
    if fecha and genero:
        peliculas = Pelicula.query.filter(Pelicula.release_date == fecha, Pelicula.genre == genero).all()
    elif fecha:
        peliculas = Pelicula.query.filter(Pelicula.release_date == fecha).all()
    elif genero:
        peliculas = Pelicula.query.filter(Pelicula.genre == genero).all()
    else:
        peliculas = Pelicula.query.all()  # Si no hay filtros, obtener todas las películas

    return render_template('index.html', peliculas=peliculas)

# Ruta para ver detalles de una película
@app.route('/pelicula/<int:id>')
def detalle_pelicula(id):
    pelicula = Pelicula.query.get(id)  # Obtener la película por su ID
    return render_template('detalle_pelicula.html', pelicula=pelicula)

# Ruta para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = Usuario.query.filter_by(email=email).first()  # Buscar usuario por correo

        if usuario and check_password_hash(usuario.password, password):  # Verificar contraseña
            login_user(usuario)
            flash("Inicio de sesión exitoso", "success")
            # Verificar si es administrador y redirigir a la página adecuada
            if usuario.is_admin:
                return redirect(url_for('panel_admin'))  # Redirigir al panel de administración si es admin
            else:
                return redirect(url_for('login'))  # Redirigir a la página principal si no es admin
        else:
            flash("Credenciales incorrectas", "danger")
    
    return render_template('login.html')


# Ruta para el panel de administración (protegida)
@app.route('/admin')
@login_required
def panel_admin():
    if not current_user.is_admin:  # Verificar si el usuario es admin
        return redirect(url_for('home'))  # Redirigir a la página principal si no es admin
    peliculas = Pelicula.query.all()  # Obtener todas las películas
    return render_template('admin_panel.html', peliculas=peliculas)


# Ruta para agregar una nueva película (protegida)
@app.route('/admin/agregar', methods=['GET', 'POST'])
@login_required
def agregar_pelicula():
    if not current_user.is_admin:  # Verificar si el usuario es admin
        return redirect(url_for('home'))  # Redirigir a la página principal si no es admin

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        genre = request.form['genre']
        duration = request.form['duration']
        release_date = request.form['release_date']
        trailer_url = request.form['trailer_url']
        sala = request.form['sala']


        # Procesar la imagen subida
        image_file = request.files['image_file']
        if image_file and allowed_file(image_file.filename):
           # Configurar Cloudinary (solo una vez)
            cloudinary.config(
                cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
                api_key=current_app.config['CLOUDINARY_API_KEY'],
                api_secret=current_app.config['CLOUDINARY_API_SECRET']
            )

            # Subir a Cloudinary
            result = cloudinary.uploader.upload(image_file)
            image_url = result['secure_url']  # Obtener la URL segura

            # Crear una nueva película en la base de datos
            nueva_pelicula = Pelicula(
                title=title,
                description=description,
                genre=genre,
                image_url=image_url,  # Guardamos la ruta del archivo en la base de datos
                duration=duration,
                release_date=release_date,
                trailer_url=trailer_url,
                sala=sala
            )
            db.session.add(nueva_pelicula)
            db.session.commit()
            flash("Película agregada correctamente", "success")
            return redirect(url_for('panel_admin'))  # Redirigir al panel de admin
        else:
            flash("El archivo de imagen no es válido", "danger")
    
    return render_template('agregar_pelicula.html')


# Ruta para editar una película (protegida)
@app.route('/admin/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_pelicula(id):
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('home'))

    pelicula = Pelicula.query.get(id)  # Obtener la película por su ID
    if request.method == 'POST':
        # Actualizar los datos de la película
        pelicula.title = request.form['title']
        pelicula.description = request.form['description']
        pelicula.genre = request.form['genre']
        pelicula.duration = request.form['duration']
        pelicula.release_date = request.form['release_date']
        pelicula.trailer_url = request.form['trailer_url']
        pelicula.sala = request.form['sala']  # ✅ Esto lo agregas también


        # Procesar la imagen subida (solo si se proporciona una nueva imagen)
        image_file = request.files.get('image_file')
        if image_file and allowed_file(image_file.filename):
            # Configurar Cloudinary (solo una vez)
            cloudinary.config(
                cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
                api_key=current_app.config['CLOUDINARY_API_KEY'],
                api_secret=current_app.config['CLOUDINARY_API_SECRET']
            )

            # Subir a Cloudinary
            result = cloudinary.uploader.upload(image_file)
            image_url = result['secure_url']  # Obtener la URL segura
            pelicula.image_url = image_url  # Actualizar la ruta de la imagen

        db.session.commit()
        flash("Película actualizada correctamente", "success")
        return redirect(url_for('panel_admin'))

    return render_template('editar_pelicula.html', pelicula=pelicula)


# Ruta para eliminar una película (protegida)
@app.route('/admin/eliminar/<int:id>', methods=['GET', 'POST'])
@login_required
def eliminar_pelicula(id):
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('home'))

    pelicula = Pelicula.query.get(id)  # Obtener la película por su ID
    db.session.delete(pelicula)
    db.session.commit()
    flash("Película eliminada correctamente", "success")
    return redirect(url_for('panel_admin'))


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Cierra la sesión del usuario
    return redirect(url_for('home'))  # Redirige a la página principal


# Función para verificar si el archivo es permitido
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS