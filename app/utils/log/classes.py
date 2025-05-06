# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/utils/log/classes.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases relacionadas con los logger de la aplicación.
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
from dataclasses import dataclass

# ---- Clases ---- #
@dataclass
class LoggerConfig:
    """
    Clase que almacena la configuración del logger.
    
    Attributes:
        level (str): Indica el nivel mínimo de severidad de los mensajes que serán registrados.
        format (str): Formato de los mensajes del log.
        datefmt (str): Formato de la fecha de los mensajes del log.
        path (str): Ruta a la carpeta de logs.
        maxBytes (int): Tamaño máximo en bytes del fichero log.
        backupCount (int): Controla cuántos archivos de respaldo se conservan al hacer rotación de logs.
    """
    # -- Parámetros -- #
    level:str = 'INFO'
    format:str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    datefmt:str = '%Y-%m-%d %H:%M:%S'
    path:str = 'logs'
    maxBytes:int = 10 * 1024 * 1024 # 10MB.
    backupCount:int = 5