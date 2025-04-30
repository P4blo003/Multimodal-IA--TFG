# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/ingestion/document_loader.py
# Autor: Pablo González García
# Descripción: Módulo de ingesta de documentación adaptado para Haystack y
# LangChain.
# -----------------------------------------------------------------------------

# -- Modulos -- #
import os
from typing import List, Literal

from utils.logger import get_logger

# Dependencias de Haystack
from haystack.document_stores.in_memory import InMemoryDocumentStore as HSInMemStore
from haystack.components.converters import MultiFileConverter
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter

# Dependencias de LangChain


# -- Clases -- #
class DocumentLoader:
    """
    Clase responsable de cargar, convertir, preprocesar e indexar documentos
    en un almacén de documentos para su posterior uso en sistemas RAG.
    """
    # Métodos por defecto #
    def __init__(self, cfg:dict):
        """
        Inicializa el cargador de documentos.
        
        :param dict cfg:
            Configuración general del sistema.
        """       
        # Inicializa las propiedades.
        self.__logger = get_logger(__name__)
        self.__backend:str = cfg.get('documents', {}).get('backend', 'haystack')
        self.__docDir:str = cfg['documents']['path']
        match self.__backend:
            case 'haystack':
                self.__store = HSInMemStore()
                self.__logger.debug("Iniciado DocumentStore de Haystack.")
            case 'langchain':
                self.__store = []
                self.__logger.debug("Iniciado DocumentStore de LangChain.")

    # Métodos públicos #
    def load_and_index(self) -> None:
        """
        Carga documentos desde el directorio configurado, los convierte a texto,
        realiza preprocesamiento y los indexa en el document store.
        """
        # Muestra información.
        self.__logger.info(f"Backend: {self.__backend.upper()} | Directorio: {self.__docDir}")
        
        # Comprueba que el directorio existe.
        if not os.path.exists(self.__docDir):
            self.__logger.error(f"Directorio inexistente: {self.__docDir}")
            return

        # Carga los documentos con haystack o langchain.
        match self.__backend:
            case 'haystack':
                pass
            case 'langchain':
                pass