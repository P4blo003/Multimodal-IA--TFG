# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/config/context.py
# Autor: Pablo González García
# Descripción:
# Módulo que se encarga de cargar la configuración del proyecto desde el 
# archivo `settings.yaml` y variables de entorno `.env`. Valida
# automáticamente la estructura.
# -----------------------------------------------------------------------------


# ---- Modulos ---- #
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

from config.schema import AppConfig


# ---- Clases ---- #
class Config:
    """
    Clase encargada de cargar, validar y proporcionar acceso a la configuración del 
    sistema.
    
    Methods:
        get() -> AppConfig:
            Devuelve el objeto de configuración validado.
    """
    # -- Métodos por defecto -- #
    def __init__(self, config_path:Path = Path("config/settings.yaml"),
                 dotenv_path:Path = Path(".env")):
        """
        Inicializa y valida la configuración desde YAML y '.venv'.
        
        Args:
            config_path (Path): Ruta al archivo YAML de configuración.
            dotenv_path (Path): Ruta al archivo `.env` con variables de entorno opcionales.
        Raises:
            FileNotFoundError: Si el archivo YAML no existe.
            ValidationError: Si el esquema no se cumple.
        """
        # Si el archivo .env existe.
        if dotenv_path.exists():
            # Carga las variables de entorno.
            load_dotenv(dotenv_path)
            self.__env = os.environ.copy()     # Copia las variables de entorno.
        # Si el archivo de configuración no existe.
        if not config_path.exists():
            # Lanza una excepción.
            raise FileNotFoundError(f"El archivo de configuración {config_path} no existe.")
        # Abre el fichero de configuración.
        with config_path.open("r", encoding="utf-8") as file:
            # Carga el contenido del fichero.
            data = yaml.safe_load(file)
        # Almacena la configuración en un atributo privado.
        self.__config:AppConfig = AppConfig(**data)
        self.__env['OLLAMA_HOST'] = f"{self.__config.ollama.host}:{self.__config.ollama.port}"
    
    # -- Métodos públicos -- #
    def getConfig(self) -> AppConfig:
        """
        Devuelve la configuración validada.
        
        Returns:
            AppConfig: Objeto de configuración validado.
        """
        return self.__config
    def getEnv(self) -> dict[str, str]:
        """
        Devuelve las variables de entorno.
        
        Returns:
            dict[str,str]: Diccionario con las variables de entorno.
        """
        return self.__env

# ---- PARÁMETROS ---- #
CONFIG:AppConfig

# ---- INICIALIZACIÓN ---- #
# Comprueba la configuración del prpoyecto y carga
# los parámetros.
configPath:Path = Path("config/settings.yaml")
if not configPath.exists():
    raise FileNotFoundError(f"El archivo de configuración {configPath} no existe.")
# Carga la configuración y variables de entorno.
__config:Config = Config(configPath)
CONFIG:AppConfig = __config.getConfig()
ENV:dict[str, str] = __config.getEnv()