import os
import secrets
from cryptography.fernet import Fernet

SECRET_DIR = os.path.join(os.getcwd(), 'static', 'secret')

# Cargar o generar la clave de cifrado Fernet
def load_fernet_key(f_key = None):
    fernet_key_path = os.path.join(SECRET_DIR, 'fernet_secret.bin')
    if not os.path.exists(fernet_key_path):
        # Si no existe, genera una nueva clave Fernet y guárdala
        if not f_key:
            fernet_key = Fernet.generate_key()
        else:
            fernet_key = f_key.encode() #Lógica para pasarlo a binario
        with open(fernet_key_path, 'wb') as archivo:
            archivo.write(fernet_key)
    else:
        # Si ya existe, lee la clave desde el archivo
        with open(fernet_key_path, 'rb') as archivo:
            fernet_key = archivo.read().decode()
    
    return Fernet(fernet_key)

# Crea el directorio para los archivos secretos si no existe
def create_secret_dir():
    if not os.path.exists(SECRET_DIR):
        os.makedirs(SECRET_DIR)

# Genera la clave de la API y la guarda cifrada
def generate_app_key():
    app_dir = os.path.join(SECRET_DIR, 'app_secret.txt')
    if not os.path.exists(app_dir):
        app_key = secrets.token_hex(16)  # Genera una clave de API aleatoria
        fernet = load_fernet_key()  # Cargar la clave de cifrado
        encrypted_key = fernet.encrypt(app_key.encode())  # Cifrar la clave de la API
        
        with open(app_dir, 'wb') as archivo:
            archivo.write(encrypted_key)  # Guarda la clave cifrada

# Cifra un texto y lo guarda en un archivo
def encrypt(filename, text):
    file_path = os.path.join(SECRET_DIR, f"{filename}.txt")
    fernet = load_fernet_key()  # Cargar la clave de cifrado
    encrypted_text = fernet.encrypt(text.encode())  # Cifra el texto
    
    with open(file_path, 'wb') as archivo:
        archivo.write(encrypted_text)  # Guarda el texto cifrado

# Desencripta el contenido de un archivo
def decrypt(filename):
    file_path = os.path.join(SECRET_DIR, f"{filename}.txt")
    fernet = load_fernet_key()  # Cargar la clave de cifrado
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as archivo:
            encrypted_text = archivo.read()  # Lee el texto cifrado
        
        decrypted_text = fernet.decrypt(encrypted_text).decode()  # Desencripta el texto
        return decrypted_text
    else:
        raise FileNotFoundError(f"{filename}.txt no encontrado")

