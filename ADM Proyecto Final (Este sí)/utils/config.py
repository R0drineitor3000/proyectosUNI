import utils.secret as secret
from authlib.integrations.flask_client import OAuth #Librería para gestionar google OAuth

class Config:
    MAIL_SERVER = 'smtp.gmail.com'  # Servidor SMTP para Gmail
    MAIL_PORT = 587  # Puerto para Gmail
    MAIL_USE_TLS = True  # Usar TLS
    MAIL_USE_SSL = False  # No usar SSL
    MAIL_USERNAME = secret.decrypt("mail")  # Tu correo de Gmail
    MAIL_PASSWORD = secret.decrypt("mail_ps")  # Tu contraseña de Gmail
    MAIL_DEFAULT_SENDER = secret.decrypt("mail")  # Correo predeterminado
    SESSION_COOKIE_HTTPONLY = True  # Evita que la cookie sea accedida por JavaScript
    SESSION_COOKIE_SECURE = True  # Asegúrate de usar HTTPS

    @staticmethod
    def get_google(oauth):
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
        return google