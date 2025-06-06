# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/utilities/logger.py
# Autor: Pablo González García
# Descripción:
# Módulo con clases y funciones relacionadas con los loggers del programa.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
import logging
from logging import Logger, Formatter
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from logging import getLogger

from config.schema import LoggerConfig


# ---- FUNCIONES ---- #
def create_logger(logger_name:str, cfg:LoggerConfig, console:bool=True, file:str=None) -> Logger:
    """
    Crea y configura una instancia de logger. Establece el nombre, formato y salida
    del logger.
    
    Args:
        logger_name (str): Nombre del logger.
        cfg (LoggerConfig): Configuración del logger.
        console (bool): True en caso de que se quiera mostrar los mensajes por consola y False en otro caso.
        file (str): Ruta relativa del fichero de log.
    Raises:
        ValueError: En caso de que algún valor sea incorrecto.
    Returns:
        Logger: Un logger configurado.
    """
    # Comprueba si los parámetros son correctos.
    if not console and not file:
        raise ValueError("Debe haber alguna salida para el logger.")    # Lanza una excepción.
    
    # Crea el logger con el nombre especificado.
    logger:Logger = getLogger(name=logger_name)
    logger.setLevel(getattr(logging, cfg.level, logging.INFO))
    logger.handlers.clear()         # Limpia todos los handlers.
    
    # Añade los handlers del logger.
    formatter:Formatter = Formatter(fmt=cfg.format, datefmt=cfg.datefmt)     # Crea el formateador.
    
    # Si se quiere un logger de consola.
    if console:
        # Crea el handler de consola.
        consoleHandler:StreamHandler = StreamHandler()
        consoleHandler.setLevel(getattr(logging, cfg.level, logging.INFO))
        consoleHandler.setFormatter(formatter)      # Añade el formatter.
        logger.addHandler(consoleHandler)             # Añade el handler al logger.

    # Si se quiere un logger de fichero.
    if file:
        # Gestiona el fichero de log.
        logDir:str = os.path.join(cfg.logDir, file)     # Crea la ruta del fichero.
        os.makedirs(os.path.dirname(logDir), exist_ok=True)           # Crea el fichero.
        # Crea el handler de fichero.
        fileHandler:RotatingFileHandler = RotatingFileHandler(logDir, maxBytes=cfg.maxBytes, backupCount=cfg.backupCount, encoding='utf-8')
        fileHandler.setLevel(getattr(logging, cfg.level, logging.INFO))
        fileHandler.setFormatter(formatter)         # Añade el formatter.
        logger.addHandler(fileHandler)                # Añade el handler al logger.

    # Devuelve el logger configurado.
    return logger