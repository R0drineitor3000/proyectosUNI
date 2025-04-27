#################################################
#################################################
######### Módulos de la Aplicación Web ##########
#################################################
#################################################

#módulos propios
import utils.secret as secret #módulo para gestionar claves y secretos
import utils.log as log #módulo para gestionar logs
from utils.config import Config #módulo para gestionar la configuración de la aplicación
from utils.user import User #módulo para gestionar los usuarios
from utils.ext import mail, oauth #módulo para gestionar extensiones de Flask

#Blueprints
from routhes.auth import auth #módulo para gestionar las rutas de inicio de sesión
from routhes.misc import misc #módulo para gestionar las rutas misceláneas
from routhes.profiles import profiles #módulo para gestionar las rutas de perfiles

#módulos propios de la base de datos
import database.accounts as accounts #módulo para gestionar las cuentas de usuario de la base de datos

#módulos varios
import atexit #módulo para ejecutar funciones al cerrar la aplicación

#módulos flask
from flask import Flask, render_template, request, session, redirect, url_for, flash #módulo para gestionar la aplicación web
from flask_login import LoginManager, current_user #módulo para gestionar el usuario logueado

#módulos para gestionar la seguridad
from werkzeug.security import generate_password_hash, check_password_hash #módulo para gestionar contraseñas
from werkzeug.utils import secure_filename #módulo para asegurar archivos

#################################################
#################################################
######### Variables de la Aplicación Web ########
#################################################
#################################################

#Configuración de la app de Flask
app = Flask(__name__) # Instancia principal de la aplicación Flask
app.secret_key = secret.decrypt("app_secret") #Clave secreta para la aplicación

#Funciones de Login Manager (Gestionan el inicio de sesión)
login_manager = LoginManager() # Instancia del LoginManager que se encargará de gestionar la autenticación de usuarios
login_manager.init_app(app) # Inicializa el LoginManager con la aplicación Flask
login_manager.login_view = 'auth.login'  # Redirige a esta vista si el usuario no está autenticado

# Flask-Login utiliza esta función para cargar el usuario desde el ID almacenado en la sesión
@login_manager.user_loader
def load_user(user_id):
    user_data = accounts.get_account(int(user_id)) #Obtiene los datos del usuario desde la base de datos
    if user_data:
        return User.from_db(user_data) #Si los datos son correctos, devuelve el usuario
    return None ##Si no, devuelve None

# Configuración de Flask
app.config.from_object(Config) #Cargar la configuración de la aplicación desde el módulo config.py
oauth.init_app(app) #Inicializa el OAuth de la app
google = Config.get_google(oauth) # Obtiene las credenciales de Google desde la configuración

mail.init_app(app) # Inicializa el mail de la app

#################################################
#################################################
######### Rutas de la Aplicación Web ############
#################################################
#################################################

# Ruta principal de la aplicación
@app.route('/')
def index():
    return render_template('index.html', user=current_user) #Renderizar la plantilla index.html

#################################################
######### Rutas de inicio de sesión #############
#################################################

app.register_blueprint(auth) #Registrar el blueprint de las rutas de sesión

#################################################
################# Rutas varias ##################
#################################################

app.register_blueprint(misc) #Registrar el blueprint de las rutas misceláneas

#################################################
############### Rutas de Perfiles ###############
#################################################

app.register_blueprint(profiles) #Registrar el blueprint de las rutas de perfiles

################################################
################## Error 404 ###################
################################################

@app.errorhandler(404) # Manejar el error 404 (Página no encontrada)
def page_not_found(error):
    return render_template('404.html', user=current_user), 404 # Renderizar la plantilla 404.html

################################################
############# Protocolo de cierre ##############
################################################

def log_shutdown(): #Función que se ejecuta al cerrar la aplicación
    log.write("Servidor desconectado") ##Escribir en el log que el servidor se ha desconectado

################################################
################################################
############# Métodos Auxiliares ###############
################################################
################################################

atexit.register(log_shutdown) #Registrar la función de cierre de sesión al cerrar la aplicación

################################################
################################################
############### Método Principal ###############
################################################
################################################
if __name__ == '__main__':
    set_debug = True # Define si la aplicación se ejecuta en modo debug (útil durante el desarrollo)
    log.initialize_log(set_debug) # Inicializar el log de la aplicación
    app.run(debug=set_debug, use_reloader=True) ## Iniciar la aplicación Flask con la configuración fijada
