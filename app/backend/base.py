

# ---- MÓDULOS ---- #
import os
from abc import ABC, abstractmethod

from yaspin import yaspin

import logging
from common.logger import get_logger

from .model import get_real_name, install_model

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
            # #TODO: Instala el modelo.
            self.__logger.info(f"Modelo embeddings {model_real_name} instalado.")                           # Imprime información.

    # -- Métodos abstractos -- #