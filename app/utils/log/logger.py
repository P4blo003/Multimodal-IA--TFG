# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/utils/log/logger.py
# Autor: Pablo González García
# Descripción:
# Módulo con clases y funciones relacionadas con los loggers del programa.
# -----------------------------------------------------------------------------

# ---- MÓDULOS ---- #
import logging.handlers
import os
import logging

from config.context import LOG_CFG


# ---- FUNCIONES ---- #
def get_logger(name:str, console:bool=True, file:str=None) -> logging.Logger:
    """
    Crea y configura un logger.
    
    Args:
        name (str): El nombre del logger a crear.
        console (bool): Si se quiere un logger de consola.
        file (str): El nombre del archivo donde escribir el log.
    Returns:
        (logging.Logger): Logger configurado.
    """
    # Comprueba si los parámetros de la función son válidos.
    if not name:                # Si no se ha pasado un nombre de logger.
        raise ValueError("No se ha pasado un nombre de logger válido.")
    
    if not console and not file:  # Si no se ha pasado un logger de consola ni de fichero.
        raise ValueError("El logger debe tener almenos un handler de consola o de fichero.")
    
    # Variables de la función.
    logger:logging.Logger = None                                # Logger a devolver.
    
    # Crea el logger conel nombre especificado.
    logger = logging.getLogger(name=name)                       # Crea el logger con el nombre,
    logger.setLevel(getattr(logging, "", logging.INFO))         # Establece el nivel del logger.
    
    # Si no tiene ningún handler. (Para evitar duplicados).
    if not logger.handlers:
        # Crea el formateador.
        formatter = logging.Formatter(fmt=LOG_CFG.format, datefmt=LOG_CFG.datefmt)
        # Si se quiere un logger de consola.
        if console:
            # Crea el handler de consola.
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, LOG_CFG.level, logging.INFO))
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)                  # Añade el handler de consola.
        
        # Si se quiere un logger de fichero.
        if file:
            # Obtiene la ruta del fichero.
            log_dir:str = os.path.join(LOG_CFG.path, file)          # Crea la ruta del fichero.
            os.makedirs(os.path.dirname(log_dir), exist_ok=True)    # Crea el fichero.
            # Crea el handler de fichero.
            file_handler = logging.handlers.RotatingFileHandler(
                log_dir, maxBytes=LOG_CFG.maxBytes, backupCount=LOG_CFG.backupCount, encoding='utf-8')
            file_handler.setLevel(getattr(logging, LOG_CFG.level, logging.INFO))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)                     # Añade el handler de fichero.
    
    # Retorna el logger.
    return logger