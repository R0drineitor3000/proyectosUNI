from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from utils.mail import send_email
from utils.secret import decrypt
from itsdangerous import URLSafeTimedSerializer

misc = Blueprint('misc', __name__)

#################################################
################# Rutas varias ##################
#################################################
@misc.route('/contact')
def contact():
    return render_template('contact.html', user=current_user)

@misc.route('/send_mail', methods=['POST'])
def send_mail():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]
    final_message = f"Enviado por {name}\nEmail: {email}\nMensaje: {message}"
    send_email(decrypt("mail"), "Mensaje desde contacto", final_message)
    return redirect(url_for('misc.contact'))