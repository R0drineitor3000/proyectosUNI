from flask_login import UserMixin, login_user
import database.accounts as accounts

class User(UserMixin):
    def __init__(self, id, username, email, password, picture, role, creation_date, active):
        self.id = str(id)  # Flask-Login requiere que `id` sea string-compatible
        self.username = username
        self.email = email
        self.password = password
        self.picture = picture
        self.role = role
        self.creation_date = creation_date
        self.active = active

    def is_active(self):
        return bool(self.active)  # Flask-Login usará esto para saber si el usuario está habilitado

    @staticmethod
    def from_db(row):
        return User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password=row['password'],
            picture=row['picture'],
            role=row['role'],
            creation_date=row['creation_date'],
            active=(int(row['active']) == 1)
        )
    

def login_user_by_email(email):
    user_data = accounts.get_account_by_email(email)
    if user_data:
        user = User.from_db(user_data)
        login_user(user)
