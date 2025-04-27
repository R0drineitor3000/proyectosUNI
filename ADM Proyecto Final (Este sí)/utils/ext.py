from flask_mail import Mail
from authlib.integrations.flask_client import OAuth
from utils.secret import decrypt

mail = Mail()
oauth = OAuth()

MAX_LOGIN_ATTEMPTS = 3 # Número máximo de intentos de inicio de sesión
LOCKOUT_TIME = 300 # 5 minutos de bloqueo

google = oauth.register(
    name='google',
    client_id=decrypt("client_id"),  # Sustituye por tu Client ID
    client_secret=decrypt("client_secret"),  # Sustituye por tu Client Secret
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    refresh_token_url=None,
    api_base_url='https://www.googleapis.com/oauth2/v3/',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',  # Añadir el jwks_uri
)