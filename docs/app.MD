# Reporte de la Aplicación Web

## Descripción General

La aplicación es una plataforma web construida con **Flask**, que incluye diversas funcionalidades como gestión de productos, perfiles de usuarios, autenticación, y comunicación con correo electrónico. La aplicación también implementa medidas de seguridad para el manejo de contraseñas y autenticación mediante OAuth2 para iniciar sesión con Google.

---

## Tecnologías Utilizadas

- **Python 3.x**
- **Flask**: Framework para construir la aplicación web.
- **Flask-Mail**: Para la gestión del correo electrónico.
- **Werkzeug**: Para funciones relacionadas con seguridad, como el hashing de contraseñas.
- **Authlib**: Para la integración con OAuth2 (Google).
- **Secrets**: Para manejar claves y contraseñas de manera segura.
- **Base de Datos**: Librerías personalizadas (`database`) para gestionar la persistencia de datos.
- **HTML/CSS/JS**: Para las interfaces de usuario.

---

## Funcionalidades Principales

### 1. **Página Principal (`/`)**
   - Muestra la página de inicio de la aplicación.
   - Registra en el log la dirección IP de quien accede.

### 2. **Perfil de Usuario (`/myprofile`)**
   - Los usuarios pueden ver y actualizar su información personal, como su nombre, correo, contraseña, biografía e imagen de perfil.
   - Implementa la validación de contraseñas y la subida de imágenes.

### 3. **Gestión de Productos (`/products` y `/upload`)**
   - Muestra una lista de productos y permite a los administradores y vendedores subir nuevos productos.
   - Los productos pueden tener imágenes asociadas.

### 4. **Autenticación de Usuario**
   - Soporta el inicio de sesión tradicional con nombre de usuario y contraseña.
   - Implementa autenticación mediante **Google OAuth2**.
   - Registra el intento de login y bloquea la cuenta temporalmente tras varios intentos fallidos.

### 5. **Confirmación de Registro (`/signin/confirm`)**
   - Los nuevos usuarios deben confirmar su registro a través de un código enviado por correo electrónico.
   - Implementa un sistema de código de autenticación y manejo de intentos fallidos.

### 6. **Notificaciones por Correo Electrónico**
   - Utiliza **Flask-Mail** para enviar correos electrónicos, como el envío de códigos de autenticación para la confirmación de usuarios.

### 7. **Gestión de Empleados (`/employees`)**
   - Permite gestionar la información de los empleados, con funcionalidades de agregar y eliminar registros.

### 8. **Logout (`/logout`)**
   - Permite a los usuarios cerrar sesión de forma segura.

### 9. **Manejo de Errores**
   - Incluye una página personalizada para manejar errores `404` de rutas no encontradas.

---

## Seguridad

- **Contraseñas**: Se utiliza `generate_password_hash` para proteger las contraseñas y `check_password_hash` para validarlas.
- **OAuth2**: Implementación de autenticación mediante Google OAuth2, que permite a los usuarios iniciar sesión con sus cuentas de Google de manera segura.
- **Bloqueo de Cuenta**: Se bloquea temporalmente la cuenta de un usuario tras tres intentos fallidos de inicio de sesión, y el bloqueo dura 5 minutos.

---

## Estructura de la Aplicación

La estructura básica del proyecto es la siguiente:

- app.py # Archivo principal de la aplicación
- database/ # Librerías para la interacción con la base de datos
- static/ # Archivos estáticos (imágenes, CSS, JS)
- templates/ # Plantillas HTML
- logs/ # Archivos de log para el seguimiento de la actividad


---

## Rutas

### `/`
- Página de inicio de la aplicación.
- Visualiza la página principal de la aplicación.

### `/myprofile`
- Página para que los usuarios gestionen su perfil.
- Se pueden actualizar el nombre, el correo, la contraseña y la foto de perfil.

### `/profiles`
- Muestra una lista de perfiles de usuarios.
- Permite realizar búsquedas por nombre o correo electrónico.

### `/upload`
- Página para que los administradores y vendedores suban productos a la plataforma.

### `/signin`
- Página para registrar nuevos usuarios.

### `/login`
- Página para que los usuarios inicien sesión en la aplicación.

---

## Observaciones

1. **Autenticación con Google OAuth2**: La integración con Google se maneja mediante la librería `Authlib`. El flujo de autenticación está bien implementado, permitiendo el acceso mediante cuentas de Google.
   
2. **Manejo de Errores y Seguridad**: La aplicación incluye un manejo adecuado de errores y bloqueo de cuentas después de intentos fallidos, lo que ayuda a proteger la cuenta de accesos no autorizados.

3. **Gestión de Archivos**: La aplicación maneja la subida de archivos de imágenes tanto para productos como para perfiles de usuario, y los guarda de forma segura utilizando `secure_filename`.

4. **Logs**: Se está utilizando una librería personalizada (`log`) para registrar todas las actividades importantes de la aplicación, como inicios de sesión, visitas y errores.

---

## Conclusión

La aplicación es una plataforma web bien estructurada para la gestión de productos y usuarios. Implementa buenas prácticas de seguridad y manejo de la información sensible. Las funcionalidades están bien definidas, y el flujo de trabajo es coherente con el objetivo general de la aplicación.
