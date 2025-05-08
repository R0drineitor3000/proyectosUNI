import os
import logging
from datetime import datetime

debug = False

def initialize_log(app_debug):
    global debug
    debug = app_debug

    # Configurar el logger solo si está habilitado el modo debug
    if debug:
        print("Debug:", str(debug))
        
        # Definir el nombre y la ruta del archivo de log
        log_name = datetime.now().strftime("%Y-%m-%d %H.%M") + ".log"
        log_dir = os.path.join(os.getcwd(), 'static', 'logs')

        # Crear el directorio si no existe
        os.makedirs(log_dir, exist_ok=True)

        log_path = os.path.join(log_dir, log_name)
        
        # Configurar el logger
        logging.basicConfig(
            filename=log_path,
            level=logging.DEBUG,  # Nivel de log, puedes cambiarlo a INFO, WARNING, etc.
            format='%(asctime)s --- %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Crear el log inicial
        logging.info(f"Archivo {log_name} creado con éxito en {log_path}")

def write(text):
    if debug:
        # Registrar el mensaje en el archivo de log
        logging.debug(text)

