# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/config/context.py
# Autor: Pablo González García
# Descripción:
# Módulo que se encarga de cargar la configuración del proyecto desde el 
# archivo `app.config.yaml` y variables de entorno `.env`. Valida
# automáticamente la estructura.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

from .schema import ServerConfig


# ---- CLASES ---- #
class ConfigManager:
    """
    Clase encargada de cargar, validar y proporcionar acceso a la configuracón del
    sistema.
    """
    # -- Métodos por defecto -- #
    def __init__(self, config_path:Path = Path("config/server.config.yaml"), dotenv_path:Path = Path(".env")):
        """
        Inicializa y valida la configuración desde `yaml` Y `.env`.
        
        Args:
            config_path (Path): Ruta al archivo YAML de configuración.
            dotenv_path (Path): Ruta al archivo `.env` con variables de entorno opcionales.
        
        Raises:
            FileNotFoundError: Si el archivo YAML no existe.
            ValidationError: Si el esquema no se cumple.
        """
        # Comrpueba si existe algún archivo de cariables de entorno. En caso de que exista, carga las variables
        # del fichero, en caso de que no exista, obtiene las variables del sistema.
        if dotenv_path.exists():
            load_dotenv(dotenv_path=dotenv_path)    # Carga las variables del fichero.
        else:
            load_dotenv()                           # Carga las variables del sistema.
        # Almacena las variables.
        self.__env:dict = os.environ.copy()         # Copia las variables.
        
        # Comprueba si el fichero de configuración existe.
        if not config_path.exists():
            raise FileNotFoundError(f"El archivo de configuración no existe. PATH: {config_path}")      # Imprime excepción.

        # Abre el fichero de configuración.
        with config_path.open('r', encoding='utf-8') as file:
            data = yaml.safe_load(file)             # Carfa el contenido.
        
        # Almacena la configuración.
        self.__config:ServerConfig = ServerConfig(**data)
        self.__env['OLLAMA_HOST'] = f"{self.Config.ollama.host}:{self.Config.ollama.port}"
    
    # -- Propiedades -- #
    @property
    def Config(self) -> ServerConfig:
        """
        Devuelve la configuración del servidor.
        
        Returns:
            AppConfig: Configuración de la aplicación.
        """
        return self.__config

    @property
    def Env(self) -> dict:
        """
        Devuelve las variables de entorno.
        
        Returns:
            dict: Variables de entorno cargadas.
        """
        return self.__env


# ---- PARÁMETROS ---- #
CFG:ServerConfig
ENV:dict


# ---- INICIALIZACIÓN ---- #
__cfgManager:ConfigManager = ConfigManager()
CFG = __cfgManager.Config
ENV = __cfgManager.Env