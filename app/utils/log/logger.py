# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/utils/log/logger.py
# Autor: Pablo González García
# Descripción:
# 
# -----------------------------------------------------------------------------

# ---- Módulos ---- #
import os

import logging
import logging.handlers

from .classes import LoggerConfig

# ---- Funciones ---- #
def get_logger(name:str, file:str, cfg:LoggerConfig) -> logging.Logger:
    """
    Crea y configura un logger co nombre especificado.
    
    Args:
        name (str): El nombre del logger a crear.
        file (str): El nombre del archivo donde escribir el log.
        cfg (LoggerConfig): Clase que almacena la configuración del logger.
    Returns:
        Logger configurado.
    """
    logger:logging.Logger = None        # Logger a devolver.
    
    # Crea el logger con el nombre.
    logger = logging.getLogger(name=name)   # Crea el logger con el nombre,
    logger.setLevel(getattr(logging, cfg.level, logging.INFO))    # Establece el nivel del logger.
    
    # Evita duplicar handlers si ya está inicializado.
    if not logger.handlers:
        # Crea el formateador.
        formatter = logging.Formatter(fmt=cfg.format, datefmt=cfg.datefmt)
        # Handler de consola.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, cfg.level, logging.INFO))
        console_handler.setFormatter(formatter)     # Establece el formato.
        logger.addHandler(console_handler)          # Añade el handler de consola.
        
        # En caso de que se quiera archvio de log.
        if file:
            log_dir:str = os.path.join(cfg.path, file)              # Crea la ruta del fichero.
            os.makedirs(os.path.dirname(log_dir), exist_ok=True)    # Crea el fichero.
            # Handler de fichero.
            file_handler = logging.handlers.RotatingFileHandler(
                log_dir, maxBytes=cfg.maxBytes, backupCount=cfg.backupCount, encoding='utf-8')
            file_handler.setLevel(getattr(logging, cfg.level, logging.INFO))
            file_handler.setFormatter(formatter)    # Establece el formato.
            logger.addHandler(file_handler)         # Añade el handler de fichero.
    
    # Devuelve el logger.
    return logger