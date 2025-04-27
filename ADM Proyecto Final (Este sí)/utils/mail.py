import random
from time import time
from flask import session
from flask_mail import Message
from utils.ext import mail

################################################
################################################
############# Códigos para email ###############
################################################
################################################

# Generador de código de autentificación para crear una cuenta
def generateAuthCode():
    session['auth_code'] = random.randint(1000, 9999)
    session['auth_code_time'] = time()  # Guardar el tiempo en que se generó el código
    session['auth_code_expiration_time'] = session['auth_code_time'] + 300  # Caducidad del código
    if 'pre_user' in session:
        pre_user = session['pre_user']
        send_auth_code_email(pre_user['email'], session['auth_code'])

# Generador de código de recuperación para cambiar la contraseña
def generateRecCode():
    session['rec_code'] = random.randint(1000, 9999)
    session['rec_code_time'] = time()  # Guardar el tiempo en que se generó el código
    session['rec_code_expiration_time'] = session['rec_code_time'] + 300  # Caducidad del código
    if "emailToConfirm" in session:
        email = session["emailToConfirm"]
        send_recover_code_email(email, session['rec_code'])

################################################
############### Envío de email #################
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
    except Exception as e:
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
    except Exception as e:
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
    except Exception as e:
        print(f'Ocurrió un error al enviar el correo: {e}')