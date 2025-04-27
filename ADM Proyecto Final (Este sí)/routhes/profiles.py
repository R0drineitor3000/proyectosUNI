import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

# Database
import database.accounts as accounts  # Módulo de la base de datos

profiles = Blueprint('profiles', __name__)

#################################################
#################################################
############### Rutas de Perfiles ###############
#################################################
#################################################

@profiles.route('/myprofile')
@login_required
def myprofile():
    return render_template('myprofile.html', user=current_user)

@profiles.route('/myprofile/edit', methods=['POST'])
@login_required
def edit_profile():
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
        if username == current_user.username:
            pass
        elif not accounts.account_exists(username):
            accounts.update_account_by_email(email, "username", username)
        else:
            flash("Ese nombre de usuario ya está tomado o no es válido", "error")

    if password is not None:
        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
        else:
            password = generate_password_hash(password, salt_length=16)
            accounts.update_account_by_email(email, "password", password)
    accounts.update_account_by_email(email, "biography", biography)
    if imagen:
        user_id = accounts.get_from_account_by_email(email, "id")
        filename = f'user_{user_id}{os.path.splitext(imagen.filename)[1]}'
            
        filename = secure_filename(filename)
            
        imagen.save(os.path.join(path, filename))
        image_path = os.path.join(path, filename)
        image_path = f"/users/{filename}"
        accounts.update_account_by_email(email, "picture", image_path)
    return redirect(url_for('profiles.myprofile'))

@profiles.route('/myprofile/delete', methods=['POST'])
@login_required
def delete_my_profile():
    accounts.update_account_by_email(current_user.email, "active", 0)
    flash("Tu cuenta ha sido eliminada.", "success")
    return redirect(url_for('auth.logout'))

@profiles.route('/profiles')
def profiles():
    users = accounts.get_all_accounts()
    return render_template('profiles.html', user=current_user, users=users)

@profiles.route('/profiles/search/<username>')
def search_profile(username):
    users = accounts.search_users(username)
    return render_template('profiles.html', user=current_user, users=users)

@profiles.route('/profiles/<username>')
def profile(username):
    user_data = accounts.get_account(username)
    return render_template('profile.html', user=current_user, user_data=user_data)