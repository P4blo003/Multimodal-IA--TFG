# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/config/settings.py
# Autor: Pablo González García
# Descripción:
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import os
from dotenv import load_dotenv

from utils.yaml import load

# ---- Clases ---- #
class LoggerSettings:
    """
    Almacena los parámetros de configuración del logger.
    
    Attributes:
        level (str): Nivel del logger.
        format (str): Formato de salida del mensaje del logger.
        datefmt (str): Formato de salida de la fecha del logger.
        path (str): Directorio de salida del logger.
        maxBytes (int): Máximo número de bytes del logger.
        backupCount (int)
    """
    # -- Parámetros por defecto -- #
    def __init__(self, file:str = "config/settings.yaml"):
        """
        Inicializa LoggerSettings y carga los datos desde el YAML.
        """
        # Inicializa los parámetros por defecto.
        self.__level:str = 'INFO'.upper()
        self.__format:str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.__datefmt:str = '%Y-%m-%d %H:%M:%S'
        self.__path:str = None
        self.__maxBytes:int = 10 * 1024 * 1024
        self.__backupCount:int = 5
        
        # Inicializa los parámetros desde el fichero de configuración.
        cfg = load(file=file, mode='r')     # Lee el fichero YAML.
        # Si se ha cargado correctamente.
        if cfg:
            logging_cfg = cfg.get('logger', {})
            # Si se han leido datos.
            if logging_cfg:
                # Obtiene los datos leidos.
                self.__level = logging_cfg.get('level', self.__level).upper()
                self.__format = logging_cfg.get('format', self.__format)
                self.__datefmt = logging_cfg.get('datefmt', self.__datefmt)
                self.__path = logging_cfg.get('path', self.__path)
                self.__maxBytes = logging_cfg.get('max_bytes', self.__maxBytes)
                self.__backupCount = logging_cfg.get('backup_count', self.__backupCount)
    
    # -- Propiedades -- #
    @property
    def Level(self) -> str:
        """
        Devuelve el nivel del logger.
        """
        return self.__level
    @property
    def Format(self) -> str:
        """
        Devuelve el formato de los mensajes del logger.
        """
        return self.__format
    @property
    def DateFmt(self) -> str:
        """
        Devuelve el formato de la fecha de los mensajes del logger.
        """
        return self.__datefmt
    @property
    def Path(self) -> str:
        """
        Devuelve el directorio de salida del logger.
        """
        return self.__path
    @property
    def MaxBytes(self) -> int:
        """
        Devuelve el máximo número de bytes del fichero.
        """
        return self.__maxBytes
    @property
    def BackupCount(self) -> int:
        """
        Devuelve el número de backups.
        """
        return self.__backupCount

class OllamaSettings:
    """
    Almacena los parámetros de configuración de ollama.
    
    Attributes:
        host (str): Host del servicio ollama.
        port (int): Puerto del servicio ollama
        bin (str): Ruta del fichero binario.
    """
    # -- Métodos por defecto -- #
    def __init__(self, file:str = "config/settings.yaml"):
        """
        Inicializa OllamaSettings y carga los datos desde el YAML.
        """
        # Inicializa los parámetros por defecto.
        self.__host:str = '0.0.0.0'
        self.__port:int = 11434
        self.__bin:str = "bin/ollama"
        
        # Inicializa los parámetros desde el fichero de configuración.
        cfg = load(file=file, mode='r')     # Lee el fichero YAML.
        # Si se ha cargado correctamente.
        if cfg:
            ollama_cfg = cfg.get('ollama', {})
            # Si se han leido datos.
            if ollama_cfg:
                # Obtiene los datos leidos.
                self.__host = ollama_cfg.get('host', self.__host)
                self.__port = ollama_cfg.get('port', self.__port)
                self.__bin = ollama_cfg.get('bin', self.__bin)
    
    # -- Propiedades -- #
    @property
    def Host(self) -> str:
        """
        Devuelve el host del servicio de ollama.
        """
        return self.__host
    @property
    def Port(self) -> int:
        """
        Devuelve el puerto del servicio de ollama.
        """
        return self.__port
    @property
    def Bin(self) -> str:
        """
        Devuelve la ruta del fichero binario.
        """
        return self.__bin

# ---- Parámetros ---- #
# Carga los valores del archivo .venv.
load_dotenv()
# Inicializa las clases de configuración.
LOGGER_SETTINGS:LoggerSettings = LoggerSettings(os.getenv('SETTINGS_FILE'))
OLLAMA_SETTINGS:OllamaSettings = OllamaSettings(os.getenv('SETTINGS_FILE'))