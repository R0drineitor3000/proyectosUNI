# Proyecto Flask - Sistema web de administración y ventas de productos agropecuarios para Finca los Castillo

Este es un proyecto basado en Flask que proporciona funcionalidades para gestionar la autenticación de usuarios, perfiles, rutas misceláneas, y más. La aplicación está configurada para manejar la seguridad, el inicio de sesión, y la interacción con la base de datos.

## Requisitos

- Python 3.x
- Flask
- Flask-Login
- werkzeug
- Otros módulos listados en `requirements.txt`

## Instalación

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   ```

2. Instala las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

3. Configura las claves y secretos en el archivo `utils/secret.py` o proporciona tus credenciales en las configuraciones de la app.

## Estructura del Proyecto

### Módulos Propios

- `utils.secret`: Gestión de claves y secretos.
- `utils.log`: Gestión de logs.
- `utils.config`: Configuración de la aplicación.
- `utils.user`: Gestión de usuarios.
- `utils.ext`: Extensiones de Flask (como `mail` y `oauth`).

### Blueprints

- `routhes.auth`: Rutas para el inicio de sesión.
- `routhes.misc`: Rutas misceláneas.
- `routhes.profiles`: Rutas para los perfiles de usuarios.

### Módulos de la Base de Datos

- `database.accounts`: Gestión de cuentas de usuarios en la base de datos.

### Otros Módulos

- `atexit`: Ejecuta funciones al cerrar la aplicación.

## Configuración

La aplicación está configurada con los siguientes elementos clave:

- **Clave secreta**: La clave secreta se obtiene a través del módulo `utils.secret`.
- **Login Manager**: Se utiliza para gestionar la autenticación de usuarios.
- **OAuth**: Configurado para la autenticación con Google, basado en las credenciales definidas en el archivo de configuración.

```python
app.secret_key = secret.decrypt("app_secret")
login_manager.login_view = 'auth.login'
oauth.init_app(app)
```

## Rutas de la Aplicación

### Ruta Principal

- `/`: Renderiza la plantilla `index.html`.

### Rutas de Inicio de Sesión

- Las rutas relacionadas con el inicio de sesión son gestionadas por el blueprint `auth`.

### Rutas Misceláneas

- Las rutas misceláneas (no asociadas directamente con la autenticación o perfiles) se gestionan mediante el blueprint `misc`.

### Rutas de Perfiles

- Las rutas para la gestión de perfiles de usuario son gestionadas a través del blueprint `profiles`.

### Error 404

- Si un usuario accede a una página no existente, se mostrará el error 404 con la plantilla `404.html`.

## Protocolos de Cierre

Cuando la aplicación se cierra, se ejecuta la función `log_shutdown` que escribe en los logs que el servidor ha sido desconectado.

```python
def log_shutdown():
    log.write("Servidor desconectado")
```

## Ejecución

Para ejecutar la aplicación, usa el siguiente comando:

```bash
python app.py
```

La aplicación se ejecutará en modo `debug` por defecto.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

