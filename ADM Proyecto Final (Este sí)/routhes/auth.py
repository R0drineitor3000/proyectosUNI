#################################################
#################################################
#############Módulos del blueprint #############
#################################################
#################################################

import secrets #Para generar tokens seguros (ej. nonces de OAuth)
from flask import Blueprint, render_template, request, redirect, url_for, flash, session #Módulos de flask
from flask_login import login_user, logout_user, login_required, current_user #Módulo para los login de flask
from werkzeug.security import generate_password_hash, check_password_hash #Módulo para encriptar contraseñas
from utils.ext import LOCKOUT_TIME, MAX_LOGIN_ATTEMPTS, google #Módulo exterior para obtener variables globales
from utils.user import User, login_user_by_email #Módulo para manejar los usuarios de flask-login
from time import time #Módulo para obtener el tiempo actual

#Database
import database.accounts as accounts #Módulo de la base de datos

auth = Blueprint('auth', __name__) #Creación del blueprint de autenticación (o registro) del usuario

#################################################
#################################################
#########Rutas de inicio de sesión #############
#################################################
#################################################

#Ruta de inicio de sesión normal
@auth.route('/login')
def login():
    if current_user.is_authenticated: #Si el usuario está autenticado, reenvía a la página principal
        return redirect(url_for('index'))
    
    #Lógica para manejar bloqueo por intentos fallidos
    if 'lockout_time' in session and session['lockout_time']: #Verifica si el tiempo de bloqueo está activo
        if time() > session['lockout_time']: #Verifica si se ha cumplido el tiempo de bloqueo
            session['attempts'] = 0 #Restaura los intentos
            session.pop('lockout_time', None) #Elimina el tiempo de bloqueo
        else:
            flash("Has excedido el número máximo de intentos. Intenta más tarde.", "error") #Impide la entrada al loging
            return redirect(url_for('index'))

    #Inicializar intentos si no existen
    if 'attempts' not in session:
        session['attempts'] = 0
        session['lockout_time'] = None
    
    #Renderizar la página
    return render_template('login.html', user=current_user)

#Obtiene los datos de '/login' y luego verifica si coinciden con las credenciales de alguna cuenta
@auth.route('/login/verify', methods=['POST'])
def verify_login():
    #Obtención de los elementos del request de '/login'
    email = request.form['email']
    password = request.form['password']

    #Obtiene los datos del usuario de la base de datos
    user_data = accounts.get_account_by_email(email)

    #En caso de que el usuario se haya encontrado, se verifica la contraseña
    if user_data and check_password_hash(user_data['password'], password):
        #Inicia sesión con el usuario seleccionado
        login_user_by_email(email)

        #Limpia los intentos
        session.pop('attempts', None)
        session.pop('lockout_time', None)

        #Redirige a la página principal
        return redirect(url_for('index'))
    #Incrementar el número de intentos fallidos en caso de que las credenciales fueran incorrectas
    session['attempts'] += 1

    #Verificar si se alcanzó el máximo de intentos fallidos
    if session['attempts'] >= MAX_LOGIN_ATTEMPTS:
        #Se bloquea el inicio de sesión por un tiempo determinado por la constante LOCKOUT_TIME
        session['lockout_time'] = time() + LOCKOUT_TIME 

        #Envía el mensaje de bloqueo al frontend
        flash("Has excedido el número máximo de intentos. Intenta más tarde.", "error")

        #Se redirige a la página principal
        return redirect(url_for('index'))
    
    #Envía el mensaje de error al frontend
    flash("Credenciales inválidas", "danger")

    #Redirige al login en caso de no poder iniciar sesión
    return redirect(url_for('auth.login'))

#Ruta de cierre de sesión
@auth.route('/logout')
@login_required #Requiere estar registrado para poder cerrar la sesión
def logout():    
    #Cierra la sesión
    logout_user()

    #Envía el mensaje de éxito al frontend
    flash("Sesión cerrada", "success")

    #Redirige a la página principal
    return redirect(url_for('index'))

#Ruta de inicio de sesión con OAuth (Inicio de sesión con google)
@auth.route('/login/oauth')
def OAuth():
    nonce = secrets.token_urlsafe(16)  #Genera un nonce
    session['nonce'] = nonce  #Guarda el nonce en la sesión
    redirect_uri = url_for('auth.callback', _external=True)
    return google.authorize_redirect(redirect_uri, nonce=nonce)  #Incluye el nonce

#Callback del OAuth, recupera información cuando se inicie sesión con google
@auth.route('/login/callback')
def callback():
    #Recuperar el nonce de la sesión
    nonce = session.get('nonce')

    #Obtiene el token de acceso y los datos del usuario
    token = google.authorize_access_token()
    try:
        #Verifica el ID token y pasa el nonce
        user = google.parse_id_token(token, nonce=nonce)
        session['user'] = user

        if (accounts.add_account(username=user.get("username"), email=user.get("email"))):
            return redirect(url_for('auth.complete'))
    except Exception as e:
        error = f"Error al validar el token: {str(e)}", "error"
        flash(f"Error al validar el token: {str(e)}", "error")
        print(error)
    return redirect(url_for('auth.complete'))

"""
    Ruta de completación del login por google
    En caso de que se inicie sesión con google por primera vez, se debe completar el registro añadiendo
    nombre de usuario, y si el usuario prefiere, también puede añadir una contraseña no ligada a google
"""
@auth.route('/login/complete', methods=['GET', 'POST'])
def complete():
    user = session.get('user')
    if request.method == 'GET':
        #En caso de que el usuario no se haya registrado con anterioridad:
        if (not accounts.is_fully_identified(user.get("email"))):
            #Se obtienen los datos obtenidos mediante la sesión de google
            email = user.get("email")
            username = user.get("username")

            #Se renderiza la página para terminar con el registro por google
            return render_template("complete.html", email=email, username=username)
        else:
            #Si el usuario ya está identificado, se reenvía directamente a la página principal
            user_data = accounts.get_account_by_email(user.get("email"))
            user = User.from_db(user_data)
            login_user(user)
            return redirect(url_for('index'))
    else: #Method POST
        #Obtiene los elementos del request en caso de POST
        username = request.form.get('username')
        password = request.form.get('password')
        #Actualiza el nombre de usuario de la cuenta
        accounts.update_account_by_email(user.get("email"), "username", username)

        #En caso de que el usuario decida poner una contraseña que no esté asociada a google
        if password is not None:
            password = generate_password_hash(password, salt_length=8)
            accounts.update_account_by_email(user.get("email"), "password", password)
            password = None

        #Termina con el procedimiento de inicio de sesión, obteniendo el usuario y limpiando datos de las cookies
        user_data = accounts.get_account_by_email(user.get("email"))
        user = User.from_db(user_data)
        login_user(user)
        session.pop('user', None)
        return redirect(url_for('profiles.myprofile'))

#################################################
##############Rutas de registro ################
#################################################

#Ruta de registro de usuario
@auth.route('/signin')
def signin():
    return render_template('signin.html', user=current_user)

#Obtiene los datos de '/signin' y luego crea una cuenta nueva
@auth.route('/signin/verify', methods=['POST'])
def verify_signin():
    #Obtiene los elementos de la solicitud de '/signin'
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    #Verificar si el usuario o email ya están registrados
    if accounts.account_exists(email):
        #Envía el mensaje de error al frontend
        flash("El email ya está registrado", "danger")
        #Redirige a la página de registro
        return redirect(url_for('auth.signin'))
    
    #Hashear la contraseña antes de insertarla
    hashed_password = generate_password_hash(password)

    #Insertar el nuevo usuario en la base de datos
    accounts.add_account(username, hashed_password, email)
    user_data = accounts.get_account_by_email(email)
    user = User.from_db(user_data)

    #Envía el mensaje de éxito al frontend
    flash("Cuenta creada exitosamente", "success")
    return redirect(url_for('auth.login'))  #Redirigir al login