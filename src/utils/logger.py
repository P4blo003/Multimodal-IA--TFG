# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/utils/logger.py
# Autor: Pablo González García
# Descripción: 
# Este módulo proporciona una función para crear e inicializar
# loggers personalizados y reutilizables. La configuración puede cargarse desde
# un archivo YAML (config/settings.yaml) o bien establecerse por defecto.
#
# El logger soporta salida por consola y archivos con rotación automática
# (RotationFileHandler). Es altamente configurable y forma parte del sistema
# centralizado de logging del asistente inteligente.
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import os
import logging
import logging.handlers

from config.settings import LOGGER_SETTINGS

# ---- Funciones ---- #
def get_logger(name:str) -> logging.Logger:
    """
    Crea y configura un logger con nombre especificado.
    Lee la configuración de logging en 'config/settings.yaml' si esta disponible,
    sino usa parámetros por defecto.
    
    Args:
        name (str): El nombre del logger a crear.
        
    Returns:
        Logger configurado.
    """
    logger:logging.Logger = None    # Logger a devolver.

    # Crea el logger con el nombre.
    logger = logging.getLogger(name=name)
    logger.setLevel(getattr(logging, LOGGER_SETTINGS.Level, logging.INFO))
    
    # Evita duplicar handlers si ya está inicializado.
    if not logger.handlers:
        # Crea el formateador.
        formatter = logging.Formatter(fmt=LOGGER_SETTINGS.Format, datefmt=LOGGER_SETTINGS.DateFmt)
        
        # Handler de consola.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOGGER_SETTINGS.Level, logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)          # Añade el handler.
        
        # Handler de archivo si se configuro.
        if LOGGER_SETTINGS.File:
            os.makedirs(os.path.dirname(LOGGER_SETTINGS.File), exist_ok=True)   # Crea el directorio.
            
            file_handler = logging.handlers.RotatingFileHandler(
                LOGGER_SETTINGS.File, maxBytes=LOGGER_SETTINGS.MaxBytes, backupCount=LOGGER_SETTINGS.BackupCount, encoding='utf-8')
            file_handler.setLevel(getattr(logging, LOGGER_SETTINGS.Level, logging.INFO))
            file_handler.setFormatter(formatter)    # Añade el handler.
            logger.addHandler(file_handler)
        
    # Devuelve el logger.
    return logger