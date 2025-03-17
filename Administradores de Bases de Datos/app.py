import log
import atexit
import secrets
import secret
import os
import database
from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = secret.decrypt("app_secret")
oauth = OAuth(app)

# Configuración de OAuth para Google
google = oauth.register(
    name='google',
    client_id=secret.decrypt("client_id"),  # Sustituye por tu Client ID
    client_secret=secret.decrypt("client_secret"),  # Sustituye por tu Client Secret
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    refresh_token_url=None,
    api_base_url='https://www.googleapis.com/oauth2/v3/',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',  # Añadir el jwks_uri
)

@app.route('/')
def home():
    client_ip = request.remote_addr
    log.write(f"Se abrió la página Homepage desde: {client_ip}")
    user = getUser()
    # Verificar si el usuario está autenticado
    return render_template('index.html', user=user)

@app.route('/profile')
def profile():
    client_ip = request.remote_addr
    user = getUser()
    log.write(f"Se abrió la página del Perfil de {user['username']} desde: {client_ip}")
    if not user:
        return redirect(url_for('home'))
    return render_template('profile.html', user = user)

@app.route('/products')
def products():
    client_ip = request.remote_addr
    log.write(f"Se abrió la página Productos desde: {client_ip}")
    productos = database.products.getAllProducts()
    user = getUser()
    for producto in productos:
        username = database.login.getUser(producto.get("idPoster")).get("username")
        if username is not None:
            producto["poster"] = username
        else:
            producto["poster"] ="Desconocido"
    if app.debug:
        return render_template('products.html', user = user, productos = productos)
    return render_template('products.html')

@app.route('/contact')
def contact():
    client_ip = request.remote_addr
    log.write(f"Se abrió la página Contactos desde: {client_ip}")
    user = getUser()
    return render_template('contact.html', user = user)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    client_ip = request.remote_addr
    log.write(f"Se abrió la página Subir Producto desde: {client_ip}")
    user = getUser()
    if request.method == 'POST':
        path = os.path.join(os.getcwd(), 'static', 'images', 'products')
        name = request.form['name']
        details = request.form['details']
        price = request.form['price']
        stock = request.form['stock']
        imagen = request.files['picture']
        product_id = database.products.getLastID()
        poster = user.get("id")
        image_path = None
        if imagen:
            filename = f'product_{product_id}{os.path.splitext(imagen.filename)[1]}'
            
            filename = secure_filename(filename)
            
            imagen.save(os.path.join(path, filename))
            image_path = os.path.join(path, filename)
            image_path = f"/products/{filename}"
        database.products.addProduct(name, price, details, stock, image_path, poster)
        return redirect(url_for('products'))
    return render_template('upload.html', user = user)

@app.route('/purchase', methods=['POST'])
def purchase():
    producto_id = request.form.get('producto_id')
    if "username" not in session:
        flash("No has iniciado sesión", "error")
        return redirect(url_for('index'))
    if producto_id:
        # Aquí puedes agregar la lógica de la compra
        log.write(f"Producto con ID {producto_id} comprado.")
        # Redirige a otra página después de la compra, por ejemplo, a un carrito de compras
        return redirect(url_for('products'))  # Cambia 'carrito' por la ruta que desees
    return redirect(url_for('products'))  # Si no se envió una ID válida, redirige al inicio

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if "username" in session:
        client_ip = request.remote_addr
        log.write(f"Se abrió la página de Inicio de Sesión desde: {client_ip}")
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('signin'))
        confirm_password = None
        password = generate_password_hash(password, salt_length=16)
        if not database.login.userExists(email) and not database.login.usernameExists(username):
            user = { "username": username, "email": email, "password": password }
            session['user'] = user
            database.login.addUser(email, username, None, password)
            log.write(f"Se creo un usuario con los siguientes datos: "+str(user))
            return redirect(url_for('complete'))
        else:
            log.write("No se pudo crear el usuario")
            flash("El correo electrónico o el usuario ya han sido tomados", "error")
            return redirect(url_for('signin'))
    else:
        client_ip = request.remote_addr
        log.write(f"Se abrió la página de Registro desde: {client_ip}")
    return render_template('signin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        client_ip = request.remote_addr
        log.write(f"Se abrió la página de Inicio de Sesión desde: {client_ip}")
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        pwhash = database.login.getUserPassword(email)
        
        if database.login.userExists(email) and check_password_hash(pwhash, password):
            username = database.login.getFromUser(email, "username")
            user = { "username": username, "email": email }
            session['user'] = user
            session['username'] = username  # Guardar el nombre de usuario en la sesión
            password = None
            client_ip = request.remote_addr
            log.write(f"{client_ip}: {email} ha iniciado sesión")
            flash(f"Datos: {session['user']}")
            return redirect(url_for('home'))
        else:
            password = None
            return "Credenciales incorrectas", 401
    return render_template('login.html')

@app.route('/login/oauth')
def OAuth():
    nonce = secrets.token_urlsafe(16)  # Genera un nonce
    session['nonce'] = nonce  # Guarda el nonce en la sesión
    redirect_uri = url_for('auth', _external=True)
    return google.authorize_redirect(redirect_uri, nonce=nonce)  # Incluye el nonce

@app.route('/login/callback')
def auth():
    # Recuperar el nonce de la sesión
    nonce = session.get('nonce')

    # Obtiene el token de acceso y los datos del usuario
    token = google.authorize_access_token()
    try:
        # Verifica el ID token y pasa el nonce
        user = google.parse_id_token(token, nonce=nonce)
        session['user'] = user
        if (database.login.addUser(user.get("email"), user.get("username"), user.get("picture"))):
            return redirect(url_for('complete'))
    except Exception as e:
        error = f"Error al validar el token: {str(e)}", "error"
        flash(f"Error al validar el token: {str(e)}", "error")
        print(error)
    return redirect(url_for('complete'))

@app.route('/login/complete', methods=['GET', 'POST'])
def complete():
    user = session.get('user')
    if not user:
        flash("No user found", "error")
        return redirect(url_for('login'))
    if request.method == 'GET':
        if (not database.login.isFullyIdentified(user.get("email"))):
            email = user.get("email")
            username = user.get("username")
            picture = user.get("picture")

            return render_template("complete.html", email=email, username=username, picture=picture)
        else: #User is fully signed in
            session['username'] = database.login.getFromUser(user.get("email"), "username")
            return redirect(url_for('profile'))
    else: #Method POST
        username = request.form.get('username')
        password = request.form.get('password')
        database.login.updateUser(user.get("email"), "username", username)
        if password is not None:
            password = generate_password_hash(password, salt_length=8)
            database.login.updateUser(user.get("email"), "password", password)
            password = None
        session['username'] = database.login.getFromUser(user.get("email"), "username")
        client_ip = request.remote_addr
        log.write(f"Se completó el registro de {{user.het('email')}} desde: {client_ip}")
        return redirect(url_for('profile'))


@app.route('/logout')
def logout():
    if 'username' in session:
        client_ip = request.remote_addr
        username = session.get("username")
        log.write(f"{client_ip}: {username} ha cerrado sesión")
    session.pop('username', None)
    session.pop('user', None)
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(error):
    user = getUser()
    return render_template('404.html', user = getUser()), 404  # Renderiza la plantilla 404.html

def log_shutdown():
    log.write("Servidor desconectado")
    database.disconnectAll()

def getUser():
    if "user" in session:
        user = session["user"]
        user["username"] = database.login.getFromUser(user.get("email"), "username")
        user["role"] = database.login.getFromUser(user.get("email"), "role")
        user["id"] = database.login.getFromUser(user.get("email"), "id")
        return user
    return None

atexit.register(log_shutdown)

if __name__ == '__main__':
    set_debug = True
    log.initialize_log(set_debug)
    app.run(debug=set_debug, use_reloader=True)
    
