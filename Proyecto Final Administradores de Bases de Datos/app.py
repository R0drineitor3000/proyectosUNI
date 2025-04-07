import log #Librería personal para gestionar el registro de actividad en la aplicación web
import atexit
import secrets #Librería Secrets
import secret #Librería personal para encriptar secrets y APIs
import os
import database #Librería personal para gestionar la base de datos
from Product import Product
import random
from time import time
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = secret.decrypt("app_secret")
oauth = OAuth(app)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Servidor SMTP para Gmail
app.config['MAIL_PORT'] = 587  # Puerto para Gmail
app.config['MAIL_USE_TLS'] = True  # Usar TLS
app.config['MAIL_USE_SSL'] = False  # No usar SSL
app.config['MAIL_USERNAME'] = secret.decrypt("mail")  # Tu correo de Gmail
app.config['MAIL_PASSWORD'] = secret.decrypt("mail_ps")  # Tu contraseña de Gmail
app.config['MAIL_DEFAULT_SENDER'] = secret.decrypt("mail")  # Correo predeterminado
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Evita que la cookie sea accedida por JavaScript
app.config['SESSION_COOKIE_SECURE'] = True  # Asegúrate de usar HTTPS

mail = Mail(app)

MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_TIME = 300

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

@app.route('/myprofile', methods=['GET', 'POST'])
def myprofile():
    client_ip = request.remote_addr
    user = getUser()
    log.write(f"Se abrió la página del Perfil de {user['username']} desde: {client_ip}")
    if not user:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        path = os.path.join(os.getcwd(), 'static', 'images', 'users')
        username = request.form["username"]
        email = request.form['email']
        imagen = request.files['profilePic']
        password = request.form['password']
        if password == "":
            password = None
        confirm_password = request.form['confirmPassword']
        biography = request.form["bio"]
        if biography == " ":
            biography = None

        if username:
            if username == user["username"]:
                pass
            elif not database.login.usernameExists(username):
                database.login.updateUser(email, "username", username)
            else:
                flash("Ese nombre de usuario ya está tomado o no es válido", "error")

        if password is not None:
            if password != confirm_password:
                flash("Las contraseñas no coinciden", "error")
            else:
                password = generate_password_hash(password, salt_length=16)
                database.login.updateUser(email, "password", password)
        database.login.updateUser(email, "biography", biography)
        if imagen:
            user_id = database.login.getFromUser(email, "id")
            filename = f'user_{user_id}{os.path.splitext(imagen.filename)[1]}'
            
            filename = secure_filename(filename)
            
            imagen.save(os.path.join(path, filename))
            image_path = os.path.join(path, filename)
            image_path = f"/users/{filename}"
            database.login.updateUser(email, "picture", image_path)
        return redirect(url_for('myprofile'))
        
    else:
        return render_template('myprofile.html', user = user)

@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
    client_ip = request.remote_addr
    user = getUser()
    log.write(f"Se abrió la página de perfiles desde: {client_ip}")
    users = None
    if request.method == 'POST':
        users = database.login.getUserLike(request.form["profilesearch"])
    else:
        users = database.login.getAllUsers()
    return render_template('profiles.html', user = user, users = users)

@app.route('/profiles/<string:username>', methods=['GET', 'POST'])
def profile(username):
    client_ip = request.remote_addr
    user = getUser()
    print(f"Se abrió la página del perfil de {username} desde: {client_ip}")
    log.write(f"Se abrió la página del perfil de {username} desde: {client_ip}")
    
    # Obtiene los datos del perfil del usuario con el username proporcionado
    profile = database.login.getUserByUsername(username)
    
    if not profile:
        flash("Perfil no encontrado", "error")
        return redirect(url_for('home'))
    
    return render_template('profile.html', user=user, profile=profile)

@app.route('/update_profile/<string:email>', methods=['POST'])
def updateProfile(email):
    profile = database.login.getUser(email)
    value = request.form["rol"]
    database.login.updateUser(email, "role", value)
    return redirect(url_for('profile', username=profile["username"]))

@app.route('/deleteProfile', methods=['POST'])
def deleteProfile():
    user = getUser()
    if user and "role" in user and user.get("role") == "admin":
        email = request.form["emailDelete"]
        database.login.deleteUser(email)
        return redirect(url_for('profiles'))
    else:
        flash("No tiene el permiso para eliminar una cuenta", "error")
        return redirect(url_for('home'))


@app.route('/products/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    client_ip = request.remote_addr
    user = getUser()
    log.write(f"Se abrió la página del producto {product_id} desde: {client_ip}")
    
    # Obtiene los datos del perfil del usuario con el ID proporcionado
    product = database.products.getProduct(product_id)
    username = database.login.getUser(product.get("idPoster")).get("username")
    if username is not None:
        product["poster"] = username
    else:
        product["poster"] ="Desconocido"
    
    if not product:
        flash("Producto no encontrado", "error")
        return redirect(url_for('home'))
    
    return render_template('product.html', user=user, product=product)

@app.route('/orders')
def orders():
    client_ip = request.remote_addr
    user = getUser()
    log.write(f"Se abrió la página de las órdenes desde: {client_ip}")
    return render_template('orders.html', user=user)

@app.route('/products', methods=['GET', 'POST'])
def products():
    client_ip = request.remote_addr
    log.write(f"Se abrió la página Productos desde: {client_ip}")
    productos = None
    if request.method == 'POST':
        productos = database.products.getProductLike(request.form["productsearch"])
    else:
        productos = database.products.getAllProducts()
    user = getUser()
    for producto in productos:
        username = database.login.getUser(producto.get("idPoster")).get("username")
        if username is not None:
            producto["poster"] = username
        else:
            producto["poster"] ="Desconocido"
    return render_template('products.html', user = user, productos = productos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    client_ip = request.remote_addr
    log.write(f"Se abrió la página Subir Producto desde: {client_ip}")
    user = getUser()
    if user["role"] != "admin" and user["role"] != "seller":
        flash("No estás autorizado para ingresar a esta página", "error")
        return redirect(url_for('products'))
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

@app.route('/purchase')
def purchase():
    if "user" not in session:
        flash("No has iniciado sesión", "error")
        return redirect(url_for('home'))
    cart = None
    if "cart" in session:
        cart = session["cart"]
    return render_template('purchase.html', user = getUser(), products=cart)

@app.route('/addtocart', methods=['POST'])
def addToCart():
    if not "user" in session:
        return redirect(url_for('login'))
    product_id = request.form['producto_id']
    ordered = request.form['ordered']
    producto = Product(product_id, ordered)
    if "cart" not in session:
        session["cart"] = {}
    session["cart"][product_id] = producto.to_dict()
    return redirect(url_for('products'))

@app.route('/cleancart')
def cleanCart():
    if "cart" in session:
        session.pop("cart", None)
    return redirect(url_for('purchase'))

@app.route('/accounts')
def accounts():
    user = getUser()
    return render_template('accounts.html', user = user)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    client_ip = request.remote_addr
    if request.method == 'POST':
        log.write(f"Se envió mensaje desde: {client_ip}")
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        final_message = f"Enviado por {name}\nEmail: {email}\nMensaje: {message}"
        send_email(secret.decrypt("mail"), "Mensaje desde contacto", final_message)
        return redirect(url_for('contact'))
    else:
        log.write(f"Se abrió la página Contactos desde: {client_ip}")
        user = getUser()
        return render_template('contact.html', user = user)

################################################
################################################
################## Empleados ###################
################################################
################################################

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'GET':
        user = getUser()
        employees = database.employees.getAllEmployees()
        for empleado in employees:
            empleado["hiredate"] = datetime.strptime(empleado["hiredate"], "%Y-%m-%d")
            empleado["birthdate"] = datetime.strptime(empleado["birthdate"], "%Y-%m-%d")
        return render_template('employees.html', user = user, employees=employees)
    else:
        given_name = request.form['given_name']
        last_name = request.form['last_name']
        birthdate = request.form['birthdate']
        hiredate = request.form['hiredate']
        idcard = request.form['idcard']
        position = request.form['position']
        salary = request.form['salary']
        database.employees.addEmployee(given_name, last_name, idcard,
                                       birthdate, hiredate, position, salary)
        return redirect(url_for('employees'))

@app.route('/deleteEmployee', methods=['POST'])
def deleteEmployee():
    idelete = request.form['idelete']
    database.employees.deleteEmployee(idelete)
    return redirect(url_for('employees'))

################################################
################################################
############# Registro de Cuenta ###############
################################################
################################################

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if "user" in session:
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
            session['pre_user'] = { "username": username, "email": email, "password": password }
            return redirect(url_for('generateAuth'))
        else:
            log.write("No se pudo crear el usuario")
            flash("El correo electrónico o el usuario ya han sido tomados", "error")
            return redirect(url_for('signin'))
    else:
        client_ip = request.remote_addr
        log.write(f"Se abrió la página de Registro desde: {client_ip}")
    return render_template('signin.html')

@app.route('/generateAuth')
def generateAuth():
    generateAuthCode()
    return redirect(url_for('confirm'))

@app.route('/signin/confirm', methods=['GET', 'POST'])
def confirm():
    pre_user = session['pre_user']
    if not session.get('pre_user') or not session.get('auth_code'):
        flash("No ha registrado ningún usuario", "error")
        return redirect(url_for('home'))
    if 'attempts' not in session:
        session['attempts'] = 0
        session['lockout_time'] = None
        
    # Lógica para manejar bloqueo por intentos fallidos
    if 'lockout_time' in session and session['lockout_time']:
        if time() > session['lockout_time']:
            session['attempts'] = 0
            session.pop('lockout_time', None)
        else:
            flash("Has excedido el número máximo de intentos. Intenta más tarde.", "error")
            return redirect(url_for('home'))
    
    # Verificar si el código ha caducado
    auth_code_time = session.get('auth_code_time')
    if auth_code_time:
        expiration_time = session['auth_code_expiration_time']
        if time() > expiration_time:
            flash("El código de autenticación ha caducado", "error")
            session.pop('pre_user', None)
            session.pop('auth_code', None)
            session.pop('auth_code_time', None)  # Limpiar los datos
            session.pop('auth_code_expiration_time', None)

    if request.method == 'POST':
        user_code = request.form['codeText']
        if user_code == str(session['auth_code']):
            user = session['pre_user']
            database.login.addUser(user['email'], user['username'], None, user['password'])
            session['user'] = user
            session.pop('pre_user', None)
            session.pop('auth_code', None)
            session.pop('auth_code_time', None)  # Limpiar los datos
            session.pop('auth_code_expiration_time', None)
            log.write(f"Se creo un usuario con los siguientes datos: {str(user)}")
            return redirect(url_for('myprofile'))
        else:
            session['attempts'] += 1
            flash("El código introducido no es válido", "error")
            if session['attempts'] >= MAX_LOGIN_ATTEMPTS:
                session['lockout_time'] = time() + LOCKOUT_TIME  # Bloqueo por un minuto
                flash("Has excedido el número máximo de intentos. Intenta más tarde.", "error")
                return redirect(url_for('home'))
            else:
                flash("El código introducido no es válido", "error")
    return render_template('confirmation.html')

################################################
################################################
############ Recuperar contraseña ##############
################################################
################################################
@app.route('/recover', methods=['POST', 'GET'])
def recover():
    user = getUser()
    if user:
        return redirect(url_for('home'))
    if request.method == 'POST':
        if not database.login.userExists(request.form["email"]):
            flash("Cuenta no registrada", "error")
            return redirect(url_for('login'))
        session["emailToConfirm"] = request.form["email"]
        return redirect(url_for('generateRec'))
    return render_template('recover.html', user=user)

@app.route('/recovercode', methods=['GET', 'POST'])
def recoverCode():
    user = getUser()
    if user or "rec_code" not in session:
        return redirect(url_for('home'))

    if 'attempts' not in session:
        session['attempts'] = 0
        session['lockout_time'] = None
        
    # Lógica para manejar bloqueo por intentos fallidos
    if 'lockout_time' in session and session['lockout_time']:
        if time() > session['lockout_time']:
            session['attempts'] = 0
            session.pop('lockout_time', None)
        else:
            flash("Has excedido el número máximo de intentos. Intenta más tarde.", "error")
            return redirect(url_for('home'))
    
    # Verificar si el código ha caducado
    rec_code_time = session.get('rec_code_time')
    if rec_code_time:
        expiration_time = session['rec_code_expiration_time']
        if time() > expiration_time:
            flash("El código de recuperación ha caducado", "error")
            session.pop('emailToConfirm', None)
            session.pop('rec_code', None)
            session.pop('rec_code_time', None)  # Limpiar los datos
            session.pop('rec_code_expiration_time', None)
            
    if "emailToConfirm" not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        rec_code = request.form["codeText"]
        if rec_code == str(session['rec_code']):
            session.pop('rec_code', None)
            session.pop('rec_code_time', None)  # Limpiar los datos
            session.pop('rec_code_expiration_time', None)
            return redirect(url_for('restore'))
        else:
            session['attempts'] += 1
            flash("El código introducido no es válido", "error")
            if session['attempts'] >= MAX_LOGIN_ATTEMPTS:
                session['lockout_time'] = time() + LOCKOUT_TIME  # Bloqueo por un minuto
                flash("Has excedido el número máximo de intentos. Intenta más tarde.", "error")
                return redirect(url_for('home'))
            else:
                flash("El código introducido no es válido", "error")
    return render_template('recovercode.html')

@app.route('/generateRec')
def generateRec():
    generateRecCode()
    return redirect(url_for('recoverCode'))

@app.route('/restore', methods=['GET', 'POST'])
def restore():
    user = getUser()
    if user:
        return redirect(url_for('home'))
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('signin'))
        confirm_password = None
        password = generate_password_hash(password, salt_length=16)
        email = session["emailToConfirm"]
        database.login.updateUser(email, "password", password)
        user = database.login.getUser(email)
        session['user'] = user
        email = None
        return redirect(url_for('myprofile'))
    return render_template('restore.html', user=user)

################################################
################################################
############## Inicio de sesión ################
################################################
################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:
        client_ip = request.remote_addr
        log.write(f"Se abrió la página de Inicio de Sesión desde: {client_ip}")
        return redirect(url_for('home'))

    # Lógica para manejar bloqueo por intentos fallidos
    if 'lockout_time' in session and session['lockout_time']:
        if time() > session['lockout_time']:
            session['attempts'] = 0
            session.pop('lockout_time', None)
        else:
            flash("Has excedido el número máximo de intentos. Intenta más tarde.", "error")
            return redirect(url_for('home'))

    # Inicializar intentos si no existen
    if 'attempts' not in session:
        session['attempts'] = 0
        session['lockout_time'] = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        pwhash = database.login.getUserPassword(email)

        if database.login.userExists(email) and check_password_hash(pwhash, password):
            username = database.login.getFromUser(email, "username")
            user = {"username": username, "email": email}
            session['user'] = user
            session['username'] = username
            session.pop('attempts', None)
            session.pop('lockout_time', None)
            client_ip = request.remote_addr
            log.write(f"{client_ip}: {email} ha iniciado sesión")
            password = None
            return redirect(url_for('home'))
        else:
            # Incrementar el número de intentos fallidos
            session['attempts'] += 1

            # Verificar si se alcanzó el máximo de intentos fallidos
            if session['attempts'] >= MAX_LOGIN_ATTEMPTS:
                session['lockout_time'] = time() + LOCKOUT_TIME  # Bloqueo por un minuto
                flash("Has excedido el número máximo de intentos. Intenta más tarde.", "error")
                return redirect(url_for('home'))

            flash("Credenciales incorrectas.", "error")
            return redirect(url_for('login'))

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
            return redirect(url_for('myprofile'))
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
        return redirect(url_for('myprofile'))


################################################
################################################
################ Cerrar Sesión #################
################################################
################################################
@app.route('/logout')
def logout():
    if 'username' in session:
        client_ip = request.remote_addr
        username = session.get("username")
        log.write(f"{client_ip}: {username} ha cerrado sesión")
    session.pop('username', None)
    session.pop('user', None)
    session.pop("cart", None)
    return redirect(url_for('home'))

################################################
################################################
################## Error 404 ###################
################################################
################################################

@app.errorhandler(404)
def page_not_found(error):
    user = getUser()
    return render_template('404.html', user = getUser()), 404  # Renderiza la plantilla 404.html

################################################
################################################
############# Protocolo de cierre ##############
################################################
################################################

def log_shutdown():
    log.write("Servidor desconectado")
    database.disconnectAll()

################################################
################################################
############# Códigos para email ###############
################################################
################################################

def generateAuthCode():
    session['auth_code'] = random.randint(1000, 9999)
    session['auth_code_time'] = time()  # Guardar el tiempo en que se generó el código
    session['auth_code_expiration_time'] = session['auth_code_time'] + 300  # Caducidad del código
    if 'pre_user' in session:
        pre_user = session['pre_user']
        send_auth_code_email(pre_user['email'], session['auth_code'])

def generateRecCode():
    session['rec_code'] = random.randint(1000, 9999)
    session['rec_code_time'] = time()  # Guardar el tiempo en que se generó el código
    session['rec_code_expiration_time'] = session['rec_code_time'] + 300  # Caducidad del código
    if "emailToConfirm" in session:
        email = session["emailToConfirm"]
        send_recover_code_email(email, session['rec_code'])

################################################
################################################
############### Envío de email #################
################################################
################################################

def send_auth_code_email(user_email, auth_code):
    #Función para enviar un correo con el código de autenticación
    msg = Message(
        'Código de autenticación',  # Asunto del correo
        recipients=[user_email],  # Destinatario
        body=f'Hola, Gracias por registrarte en MilkManager.\nPara completar tu registro, debes escribir tu código de autenticación. tu código es: {auth_code}'  # Cuerpo del mensaje
    )
    
    try:
        # Enviar el correo
        mail.send(msg)
        print(f"Correo enviado con éxito a {user_email}")
        log.write(f'Correo enviado a {user_email} con el código de autenticación')
    except Exception as e:
        log.write(f'Correo enviado a {user_email} con el código de autenticación')
        print(f'Ocurrió un error al enviar el correo: {e}')

def send_recover_code_email(user_email, auth_code):
    #Función para enviar un correo con el código de autenticación
    msg = Message(
        'Código de restauración',  # Asunto del correo
        recipients=[user_email],  # Destinatario
        body=f'¿Has olvidado tu contraseña? Ingresa este código para recuperarla:\n{auth_code}'  # Cuerpo del mensaje
    )
    
    try:
        # Enviar el correo
        mail.send(msg)
        print(f"Correo enviado con éxito a {user_email}")
        log.write(f'Correo enviado a {user_email} con el código de autenticación')
    except Exception as e:
        log.write(f'Correo enviado a {user_email} con el código de autenticación')
        print(f'Ocurrió un error al enviar el correo: {e}')

def send_email(user_email, affair, text):
    #Función para enviar un correo con el código de autenticación
    msg = Message(
        affair,  # Asunto del correo
        recipients=[user_email],  # Destinatario
        body=text  # Cuerpo del mensaje
    )
    
    try:
        # Enviar el correo
        mail.send(msg)
        print(f"Correo enviado con éxito a {user_email}")
        log.write(f'Correo enviado a {user_email} con el código de autenticación')
    except Exception as e:
        log.write(f'Correo enviado a {user_email} con el código de autenticación')
        print(f'Ocurrió un error al enviar el correo: {e}')

################################################
################################################
############# Métodos Auxiliares ###############
################################################
################################################

def getUser():
    if "user" in session:
        user = session["user"]
        user["username"] = database.login.getFromUser(user.get("email"), "username")
        user["picture"] = database.login.getFromUser(user.get("email"), "picture")
        user["role"] = database.login.getFromUser(user.get("email"), "role")
        user["biography"] = database.login.getFromUser(user.get("email"), "biography")
        user["id"] = database.login.getFromUser(user.get("email"), "id")
        return user
    return None

def obtainUser(email):
    obtainedUser = None
    if database.login.userExists(email):
        obtainedUser = {}
        obtainedUser["email"] = email
        obtainedUser["username"] = database.login.getFromUser(email, "username")
        obtainedUser["role"] = database.login.getFromUser(email, "role")
        obtainedUser["picture"] = database.login.getFromUser(email, "picture")
        obtainedUser["biography"] = database.login.getFromUser(email, "biography")
        obtainedUser["id"] = database.login.getFromUser(email, "id")
    return obtainedUser

atexit.register(log_shutdown)

################################################
################################################
#################### Main ######################
################################################
################################################

if __name__ == '__main__':
    set_debug = True
    log.initialize_log(set_debug)
    app.run(debug=set_debug, use_reloader=True)
    
