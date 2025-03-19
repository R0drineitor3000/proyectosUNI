# Librería de gestión de usuarios en SQLite

Esta librería proporciona métodos para interactuar con una base de datos SQLite para gestionar usuarios. Permite realizar operaciones como agregar, actualizar, eliminar, y obtener usuarios, así como algunas funciones de administración de la base de datos.

## Funciones

### `connect()`

Establece una conexión a la base de datos `database.db` si aún no se ha realizado. La conexión se mantiene globalmente en la variable `conn`. Se asegura de que la misma conexión sea utilizada en diferentes hilos.

### `disconnect()`

Cierra la conexión a la base de datos si está activa, y establece la variable `conn` a `None`.

### `addUser(email, username=None, picture=None, password=None, role="customer")`

Agrega un nuevo usuario a la base de datos. Si el usuario ya existe (basado en el email), no se realiza ninguna acción.

- **Parámetros**:
  - `email` (str): El correo electrónico del usuario (obligatorio).
  - `username` (str, opcional): Nombre de usuario (opcional).
  - `picture` (str, opcional): URL o ruta a la imagen del usuario (opcional).
  - `password` (str, opcional): Contraseña del usuario (opcional, solo necesaria si no se registra mediante Google).
  - `role` (str, opcional): Rol del usuario (por defecto es `"customer"`).

- **Retorna**: 
  - `True` si el usuario fue agregado correctamente.
  - `False` si el usuario ya existe.

### `updateUser(email, field, data)`

Actualiza un campo de un usuario en la base de datos.

- **Parámetros**:
  - `email` (str): El correo electrónico del usuario a actualizar.
  - `field` (str): El campo a actualizar (uno de `'id'`, `'email'`, `'username'`, `'password'`, `'role'`, `'picture'`).
  - `data` (str): El nuevo valor para el campo especificado.

- **Retorna**: 
  - `True` si la actualización fue exitosa.
  - `False` si el campo no es válido o si el usuario no existe.

### `deleteUser(email)`

Elimina un usuario de la base de datos.

- **Parámetros**:
  - `email` (str): El correo electrónico del usuario a eliminar.

- **Retorna**: 
  - `True` si el usuario fue eliminado correctamente.
  - `False` si el usuario no existe.

### `isFullyIdentified(email)`

Verifica si un usuario tiene todos los campos necesarios completos (excepto la contraseña y la imagen, que son opcionales para usuarios registrados a través de Google).

- **Parámetros**:
  - `email` (str): El correo electrónico del usuario a verificar.

- **Retorna**:
  - `True` si el usuario está completamente identificado.
  - `False` si el usuario falta de algún campo requerido.

### `getFromUser(email, field)`

Obtiene el valor de un campo específico de un usuario.

- **Parámetros**:
  - `email` (str): El correo electrónico del usuario.
  - `field` (str): El campo a obtener (uno de `'id'`, `'email'`, `'username'`, `'password'`, `'role'`, `'picture'`).

- **Retorna**:
  - El valor del campo solicitado, o `None` si el campo no existe o el usuario no es encontrado.

### `getUsers()`

Obtiene todos los usuarios de la base de datos.

- **Retorna**: Una lista con los registros de todos los usuarios.

### `getAllUsers()`

Obtiene todos los usuarios de la base de datos y los convierte en un formato de diccionario.

- **Retorna**: Una lista de diccionarios con la información de todos los usuarios.

### `getUser(ID)`

Obtiene la información de un usuario basado en su `email` o `id`.

- **Parámetros**:
  - `ID` (str | int): Puede ser el `email` del usuario (str) o su `id` (int).

- **Retorna**: Un diccionario con los datos del usuario, o `None` si no se encuentra.

### `userExists(email)`

Verifica si un usuario con el correo electrónico especificado ya existe en la base de datos.

- **Parámetros**:
  - `email` (str): El correo electrónico del usuario.

- **Retorna**: 
  - `True` si el usuario existe.
  - `False` si el usuario no existe.

### `usernameExists(username)`

Verifica si un nombre de usuario ya está en uso.

- **Parámetros**:
  - `username` (str): El nombre de usuario a verificar.

- **Retorna**: 
  - `True` si el nombre de usuario ya está en uso.
  - `False` si el nombre de usuario no está en uso.

### `getUserPassword(email)`

Obtiene la contraseña de un usuario basado en su correo electrónico.

- **Parámetros**:
  - `email` (str): El correo electrónico del usuario.

- **Retorna**: La contraseña del usuario si existe, o `None` si el usuario no se encuentra.

### Funciones de depuración (solo para desarrollo)

#### `clearUsers()`

Elimina todos los usuarios de la base de datos y realiza un `VACUUM` para optimizar el espacio.

#### `createTable()`

Crea la tabla `accounts` en la base de datos con las columnas necesarias.

#### `deleteTable()`

Elimina la tabla `accounts` de la base de datos.

#### `getStructure()`

Imprime la estructura de la tabla `accounts` mostrando los nombres y tipos de las columnas.

---

## Dependencias

- `sqlite3`: Para interactuar con la base de datos SQLite.

---

## Notas

- La conexión con la base de datos se maneja de forma global a través de la variable `conn`. 
- Asegúrate de llamar a `connect()` antes de utilizar cualquier método que interactúe con la base de datos.
- Para facilitar el desarrollo, algunas funciones de depuración están disponibles, pero deben eliminarse antes de lanzar la librería en producción.
