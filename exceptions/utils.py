import logging
import os
import datetime
import traceback

# Configuración básica del logger
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logging.basicConfig(filename=os.path.join(log_folder, 'app.log'), level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_exception_with_object(exception_name, custom_object={}):
    try:
        # Obtener la fecha actual
        date_today = datetime.datetime.now().date()

        # Crear el nombre del archivo de registro
        log_filename = f"{date_today}_with_object.log"
        log_path = os.path.join(log_folder, log_filename)

        # Si el archivo de registro para hoy no existe, crearlo
        if not os.path.exists(log_path):
            with open(log_path, 'w'):
                pass

        # Configurar el logger para registrar en el archivo correspondiente
        logger = logging.getLogger(log_filename)
        fh = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Obtener la traza de pila de la excepción
        traceback_info = traceback.format_exc()

        # Registrar la excepción con la información de traceback y el objeto
        if exception_name:
            logger.error(f"Exception: {str(exception_name)}, Custom Object: {custom_object}, Traceback: {traceback_info},  Date:{date_today}")
        else:
            logger.error(f"Exception: {exception_name}, Custom Object: {custom_object}, Traceback: {traceback_info},  Date:{date_today}")
    except Exception as e:
        print(f"Error al registrar la excepción: {e}")
