# Librería de cifrado y manejo de claves secretas

Esta librería proporciona funciones para generar, cifrar y desencriptar claves secretas y otros datos. Utiliza la biblioteca `cryptography` para realizar el cifrado y almacenamiento seguro de las claves.

## Funciones

### `load_fernet_key()`

Carga la clave de cifrado Fernet desde un archivo o genera una nueva clave si no existe.

- **Retorna**:
  - Un objeto `Fernet` que se usa para cifrar y descifrar datos.

- **Efectos secundarios**:
  - Si el archivo `fernet_secret.txt` no existe en el directorio `static/secret`, genera una nueva clave Fernet y la guarda en el archivo.
  - Si el archivo ya existe, lee la clave desde el archivo.

### `create_secret_dir()`

Crea el directorio `static/secret` si no existe, donde se almacenarán las claves y otros archivos secretos.

- **Efectos secundarios**:
  - Si el directorio no existe, lo crea para poder almacenar los archivos relacionados con el cifrado y las claves.

### `generate_app_key()`

Genera una clave de API aleatoria, la cifra con la clave Fernet y la guarda en un archivo.

- **Efectos secundarios**:
  - Si el archivo `app_secret.txt` no existe en el directorio `static/secret`, se genera una clave de API aleatoria (16 bytes) y se cifra con la clave Fernet.
  - Guarda la clave cifrada en el archivo `app_secret.txt`.

### `encrypt(filename, text)`

Cifra un texto y lo guarda en un archivo.

- **Parámetros**:
  - `filename` (str): El nombre del archivo donde se guardará el texto cifrado (sin extensión).
  - `text` (str): El texto que se desea cifrar.

- **Efectos secundarios**:
  - El texto se cifra utilizando la clave Fernet y se guarda en un archivo con el nombre `filename.txt` en el directorio `static/secret`.

### `decrypt(filename)`

Desencripta el contenido de un archivo previamente cifrado.

- **Parámetros**:
  - `filename` (str): El nombre del archivo que contiene el texto cifrado (sin extensión).

- **Retorna**:
  - El texto descifrado (str).

- **Excepciones**:
  - Lanza una excepción `FileNotFoundError` si el archivo `filename.txt` no existe en el directorio `static/secret`.

---

## Dependencias

- `os`: Para interactuar con el sistema de archivos y crear directorios.
- `secrets`: Para generar claves aleatorias de manera segura.
- `cryptography.fernet`: Para realizar el cifrado y descifrado utilizando el esquema Fernet.

---

## Notas

- Los archivos secretos se almacenan en el directorio `static/secret`, y los nombres de los archivos incluyen una extensión `.txt`.
- La clave de cifrado Fernet es generada y almacenada en `fernet_secret.txt`. Asegúrate de proteger este archivo, ya que es necesario para descifrar cualquier dato cifrado.
- Si el archivo de clave de API (`app_secret.txt`) ya existe, la función `generate_app_key()` no genera una nueva clave, sino que reutiliza la existente.
- Es recomendable mantener este sistema de almacenamiento y cifrado en un entorno seguro, especialmente para las claves sensibles como las de la API.
