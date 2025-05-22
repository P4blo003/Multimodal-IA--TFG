# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/backend/base.py
# Autor: Pablo González García
# Descripción: 
# Módulo que define la clase base 'LAMBackend' para la gestión del backend
# de la aplicación. Esta clase abstracta establece la estructura básica,
# la comprobación e instalación del modelo de embeddings.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
from abc import ABC, abstractmethod
from yaspin import yaspin

import logging
from common.logger import get_logger

from huggingface.model import get_real_name, install_model

from config.context import CONFIG


# ---- CLASES ---- #
class LAMBackend(ABC):
    """
    Esta clase representa la clase base para el backend de la aplicación.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la clase.
        """
        # Inicializa los parámetros.
        self.__logger:logging.Logger = get_logger(name=__name__, file="app.log", console=False)
        # Comprueba que exista el modelo y lo instala en caso de que no exista.
        self.__check_model()
    
    
    # -- Propiedades -- #
    @property
    def Logger(self) -> logging.Logger:
        """
        Devuelve el logger de la clase.
        """
        return self.__logger
    @property
    def ModelPath(self) -> str:
        """
        Devuelve el directorio del modelo.
        
        Returns:
            str: El directorio del modelo.
        """
        return self.__modelPath

    # -- Métodos privados -- #
    def __check_model(self):
        """
        Comprueba que el modelo de embeddings este instalado y en caso de que no lo este, lo instala.
        """
        # Genera la ruta.
        path = os.path.join(CONFIG.rag.modelDirectory, CONFIG.rag.embeddingModel)
        # Si el directorio no existe.
        if not os.path.exists(path=path):
            model_real_name:str = get_real_name(CONFIG.rag.embeddingModel)
            self.__logger.warning(f"Modelo embeddings {model_real_name} no encontrado. Instalando ...")     # Imprime información.
            with yaspin(text=f"Instalando modelo {CONFIG.rag.embeddingModel} ...") as sp:
                self.__modelPath:str = install_model(model=CONFIG.rag.embeddingModel, dir=path,silent=True)
            # Si se ha devuelto la ruta del modelo.
            if self.__modelPath:
                self.__logger.info(f"Modelo embeddings {model_real_name} instalado. PATH: {self.__modelPath}")  # Imprime información.
            else:
                self.__logger.error(f"No se pudo descargar el modelo {model_real_name}.")                       # Imprime información.

    # -- Métodos abstractos -- #
    @abstractmethod
    def IndexDocuments(self):
        """
        Indexa los documentos.
        """
        pass