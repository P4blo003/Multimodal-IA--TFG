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

class DocumentLoaderSettings:
    """
    Almacena los parámetros de configuración del cargador de
    documentos.
    
    Attributes:
        backend (str): El backend que se emplea.
        path (str): La ruta de donde se obtienen los ficheros.
        validExtensions (list): Lista con las extensiones válidas de los ficheros.
        persist (bool): Si se deben almacenar las indexaciones.
        persistPath (str): La ruta de persistencia de las indexaciones.
    """
    # -- Parámetros por defecto -- #
    def __init__(self, file:str = "config/settings.yaml"):
        """
        Inicializa LoggerSettings y carga los datos desde el YAML.
        """
        # Inicializa los parámetros por defecto.
        self.__backend:str = "Haystack"
        self.__path:str = "data/raw"
        self.__validExtensions:list = []
        self.__persist:bool = False
        self.__persistPath:str = None
        
        # Inicializa los parámetros desde el fichero de configuración.
        cfg = load(file=file, mode='r')     # Lee el fichero YAML.
        # Si se ha cargado correctamente.
        if cfg:
            logging_cfg = cfg.get('documentLoader', {})
            # Si se han leido datos.
            if logging_cfg:
                # Obtiene los datos leidos.
                self.__backend = logging_cfg.get('backend', self.__backend)
                self.__path = logging_cfg.get('path', self.__path)
                self.__validExtensions = logging_cfg.get('validExtensions', self.__validExtensions)
                self.__persist = logging_cfg.get('persist', self.__persist)
                self.__persistPath = logging_cfg.get('peristPath', self.__persistPath)
    
    # -- Propiedades -- #
    @property
    def Backend(self) -> str:
        """
        Devuelve el backend empleado.
        """
        return self.__backend
    @property
    def Path(self) -> str:
        """
        Devuelve el directorio de los archivos.
        """
        return self.__path
    @property
    def ValidExtensions(self) -> list:
        """
        Devuelve el listado con las extensiones válidas.
        """
        return self.__validExtensions
    @property
    def Persist(self) -> bool:
        """
        Devuelve si se debe mantener la persistencia de las indexaciones.
        """
        return self.__persist
    @property
    def PersistPath(self) -> str:
        """
        Devuelve la ruta donde almacenar las indexaciones.
        """
        return self.__persistPath

# ---- Parámetros ---- #
# Carga los valores del archivo .venv.
load_dotenv()
# Inicializa las clases de configuración.
LOGGER_SETTINGS:LoggerSettings = LoggerSettings(os.getenv('SETTINGS_FILE'))
DOCUMENT_LOADER_SETTINGS:DocumentLoaderSettings = DocumentLoaderSettings(os.getenv('SETTINGS_FILE'))