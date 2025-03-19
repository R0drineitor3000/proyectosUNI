# Librería de gestión de logs

Esta librería proporciona métodos para inicializar y escribir logs en un archivo. Es útil para el seguimiento y depuración de aplicaciones, y se activa solo cuando el modo de depuración (`debug`) está habilitado.

## Funciones

### `initialize_log(app_debug)`

Inicializa la configuración del logger según el valor del modo de depuración (`app_debug`). Si el modo de depuración está habilitado, se creará un archivo de log donde se almacenarán los mensajes de debug.

- **Parámetros**:
  - `app_debug` (bool): Valor que indica si el modo de depuración está habilitado (`True`) o deshabilitado (`False`).

- **Efectos secundarios**:
  - Si `app_debug` es `True`, se crea un archivo de log en la ruta `static/logs` con el nombre basado en la fecha y hora actuales.
  - Se configura el nivel del logger como `DEBUG`, y el formato del log incluye la fecha, hora y mensaje.
  - Si el directorio `static/logs` no existe, se crea automáticamente.

### `write(text)`

Escribe un mensaje en el archivo de log si el modo de depuración está habilitado.

- **Parámetros**:
  - `text` (str): El mensaje que se desea escribir en el archivo de log.

- **Efectos secundarios**:
  - Si el modo de depuración está habilitado (`debug` es `True`), se registra el mensaje en el archivo de log configurado.
  - El mensaje se registra con nivel `DEBUG` y el formato especificado en la configuración del logger.

---

## Dependencias

- `os`: Para interactuar con el sistema de archivos y crear directorios si es necesario.
- `logging`: Para la creación y configuración del sistema de logs.
- `datetime`: Para generar nombres de archivos basados en la fecha y hora actuales.

---

## Notas

- La configuración del logger se realiza solo si el modo de depuración está habilitado (es decir, si `debug` es `True`).
- Los archivos de log se guardan en el directorio `static/logs` dentro del directorio de trabajo actual. Si el directorio no existe, se crea automáticamente.
- El formato de los logs incluye la fecha y hora en que se registra el mensaje.

---
