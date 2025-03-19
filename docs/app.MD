# Documentación del Código de la Aplicación Flask

## Descripción General

Esta aplicación Flask está diseñada para gestionar usuarios, autenticación, productos y compras. Implementa la funcionalidad de inicio de sesión (tanto tradicional como mediante OAuth con Google), así como un sistema para administrar productos y mostrar información relevante en diferentes páginas del sitio. La aplicación también maneja la seguridad de inicio de sesión con un límite de intentos fallidos y la validación del correo electrónico.

## Módulos Importados

- **log**: Módulo para registrar los logs de las acciones del sistema.
- **atexit**: Se utiliza para ejecutar funciones al cerrar el servidor, como desconectar la base de datos.
- **secrets**: Generación de tokens seguros y aleatorios para la autenticación.
- **secret**: Contiene información sensible, como claves de la aplicación.
- **os**: Interactúa con el sistema de archivos para guardar imágenes de productos.
- **database**: Interacción con la base de datos para obtener, agregar y modificar usuarios y productos.
- **time**: Proporciona la función `time()` para gestionar el tiempo y el bloqueo por intentos fallidos.
- **flask**: El framework principal para la creación de la aplicación web, que incluye funcionalidades como `Flask`, `render_template`, `request`, `session`, etc.
- **werkzeug.security**: Funciones para la gestión segura de contraseñas: `generate_password_hash` y `check_password_hash`.
- **werkzeug.utils**: Utilidades para gestionar archivos, como `secure_filename` para evitar nombres de archivos inseguros.
- **authlib.integrations.flask_client**: Para la implementación de OAuth con Google.

## Constantes

- **MAX_LOGIN_ATTEMPTS**: Número máximo de intentos fallidos de inicio de sesión antes de bloquear temporalmente al usuario.
- **LOCKOUT_TIME**: Tiempo de bloqueo en segundos (300 segundos o 5 minutos) tras alcanzar el máximo de intentos fallidos.

## Configuración de OAuth

- La aplicación usa **OAuth** con Google para la autenticación de usuarios.
- Se registra el cliente de Google con las claves de cliente y secreto descifradas, y se configuran las URLs de autorización y token, así como el `jwks_uri` para obtener las claves públicas.

## Rutas (Endpoints)

### 1. `/` (Página Principal)

- **Método**: `GET`
- **Descripción**: Muestra la página principal (`index.html`). Si el usuario está autenticado, muestra su información.
- **Funcionalidad**: Registra la IP del usuario que accede.

### 2. `/profile` (Perfil del Usuario)

- **Método**: `GET`
- **Descripción**: Muestra la página del perfil del usuario autenticado.
- **Funcionalidad**: Si el usuario no está autenticado, redirige a la página principal.

### 3. `/products` (Productos)

- **Método**: `GET`
- **Descripción**: Muestra todos los productos disponibles en la base de datos.
- **Funcionalidad**: Obtiene la lista de productos y sus detalles. Si el producto tiene un "poster" (usuario que lo publicó), lo asigna a la lista.

### 4. `/contact` (Página de Contacto)

- **Método**: `GET`
- **Descripción**: Muestra la página de contacto.

### 5. `/upload` (Subir Producto)

- **Método**: `GET`, `POST`
- **Descripción**: Permite a los usuarios con rol "admin" o "seller" subir nuevos productos.
- **Funcionalidad**: Se valida que el usuario esté autorizado y se guarda el producto con la información proporcionada, incluyendo la imagen del producto.

### 6. `/purchase` (Comprar Producto)

- **Método**: `POST`
- **Descripción**: Maneja la compra de un producto.
- **Funcionalidad**: Registra la compra del producto y redirige al usuario a la página de productos.

### 7. `/signin` (Registro de Usuario)

- **Método**: `GET`, `POST`
- **Descripción**: Permite registrar un nuevo usuario con su nombre de usuario, correo electrónico y contraseña.
- **Funcionalidad**: Se valida que las contraseñas coincidan y que el usuario o correo electrónico no estén en uso.

### 8. `/login` (Inicio de Sesión)

- **Método**: `GET`, `POST`
- **Descripción**: Permite que los usuarios inicien sesión con su correo electrónico y contraseña.
- **Funcionalidad**: Gestiona el bloqueo por intentos fallidos y redirige al usuario si la autenticación es exitosa.

### 9. `/login/oauth` (Redirección de OAuth)

- **Método**: `GET`
- **Descripción**: Inicia el proceso de inicio de sesión mediante OAuth con Google.
- **Funcionalidad**: Genera un `nonce` y redirige al usuario a la autorización de Google.

### 10. `/login/callback` (Callback de OAuth)

- **Método**: `GET`
- **Descripción**: Recibe el token de acceso de Google después de la autenticación.
- **Funcionalidad**: Verifica el token, guarda los detalles del usuario en la sesión y lo agrega a la base de datos si es necesario.

### 11. `/login/complete` (Completar Registro)

- **Método**: `GET`, `POST`
- **Descripción**: Permite al usuario completar su registro después de iniciar sesión mediante OAuth.
- **Funcionalidad**: Permite al usuario configurar su nombre de usuario y contraseña. Si la información está completa, se redirige al perfil.

### 12. `/logout` (Cerrar Sesión)

- **Método**: `GET`
- **Descripción**: Cierra la sesión del usuario autenticado.
- **Funcionalidad**: Elimina la sesión del usuario y redirige a la página principal.

### 13. `/404` (Página de Error 404)

- **Método**: `GET`
- **Descripción**: Muestra una página de error 404 si la ruta solicitada no existe.

## Funciones Auxiliares

### `log_shutdown()`

- **Descripción**: Registra el cierre del servidor y desconecta de la base de datos al finalizar.

### `getUser()`

- **Descripción**: Recupera la información del usuario autenticado desde la sesión, incluyendo su nombre de usuario, rol y ID.

## Manejo de Seguridad

- **Bloqueo por Intentos Fallidos**: Si un usuario supera el número máximo de intentos fallidos, se bloquea temporalmente (por 5 minutos) para evitar ataques de fuerza bruta.
- **Hashing de Contraseñas**: Las contraseñas se almacenan de manera segura utilizando un hash (con `generate_password_hash` y `check_password_hash`).
- **OAuth con Google**: Proporciona un método de inicio de sesión alternativo con OAuth 2.0.

## Desarrollo y Configuración

- **Modo Debug**: La aplicación se ejecuta en modo de depuración (`debug=True`), lo que facilita el desarrollo.
- **Logs**: Se registra la actividad del servidor en el archivo de log especificado, lo que ayuda a rastrear el acceso y las acciones realizadas por los usuarios.
