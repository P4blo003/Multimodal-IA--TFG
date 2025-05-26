# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/backend/manager.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene las clases encargadas de gestionar el backend del 
# programa, como el sistema RAG o prompting.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ----- #
from abc import ABC
from abc import abstractmethod

from yaspin import yaspin

from logging import Logger
from common.logger import create_logger

from chat.history import ChatHistory

from external.huggingFace.model import model_installed, install_model

from config.context import CFG


# ---- CLASES ---- #
class BackendManager(ABC):
    """
    Instancia base que se encarga de manejar todo lo relacionado con el backend del sistema.
    Se encarga de gestionar el RAG y prompting.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la instancia.
        """
        # Inicializa las propiedades.
        self.__logger:Logger = create_logger(logger_name=__name__, console=False, file="app.log")
        self.__check_embedding_model()      # Comprueba que el modelo de embedding esté instalado.
    
    # -- Propiedades -- #
    @property
    def Logger(self) -> Logger:
        """
        Devuelve el logger del manager.
        
        Returns:
            Logger: El logger del manager.
        """
        return self.__logger
        
    # -- Métodos privados -- #
    # -- Métodos públicos -- #
    def __check_embedding_model(self) -> any:
        """
        Comprueba si el modelo de embedding esta instalado y en caso de que no lo esté,
        lo instala.
        """
        # Comprueba si el modelo está instalado.
        if not model_installed(model_name=CFG.rag.embedding.model, json_path=CFG.rag.embedding.file):
            
            self.Logger.warning(f"El modelo {CFG.rag.embedding.model} no esta instalado. Instalando ...")    # Imprime información.

            with yaspin(text=f"Instalando modelo {CFG.rag.embedding.model} ...") as sp:
                path:str = install_model(model_name=CFG.rag.embedding.model, json_path=CFG.rag.embedding.file, dir=CFG.rag.embedding.persistDirectory) # Instala el modelo.

            self.Logger.info(f"Modelo {CFG.rag.embedding.model} instalado. PATH: {path}")                     # Imprime información.

    # -- Métodos abstractos -- # 
    @abstractmethod
    def EmbedDocuments(self) -> any:
        """
        Realiza el embedding de los documentos.
        """   
        pass

    @abstractmethod
    def BuildPrompt(self, user_input:str, history:ChatHistory) -> str:
        """
        Construye el prompt a partir del contexto, historial y query.
        
        Args:
            user_input (str): Input del usuario.
            history (ChatHistory): Historial del chat.
            
        Returns:
            str: El prompt construido.
        """
        pass