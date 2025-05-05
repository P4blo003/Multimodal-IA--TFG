# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/config/settings.py
# Autor: Pablo González García
# Descripción:
# Módulo para cargar, preprocesar e indexar documentos en tiempo de ejecución.
# -----------------------------------------------------------------------------

# ---- Módulos ---- #
from config.settings import DOCUMENT_LOADER_SETTINGS
from utils.logger import get_logger

#Haystack.
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack_integrations.document_stores.weaviate import WeaviateDocumentStore

# ---- Clases ---- #
class DocumentLoader():
    """
    Clase encargada de cargar y procesar documentos desde un directorio dado.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa el cargador de documentos.
        
        Args:

        """
        # Inicializa los parámetros por defecto.
        self.__logger = get_logger(__name__)        # Crea el logger para el script document_loader.
        self.__store = None
        
        self.__logger.info(f"Inicializado: BACKEND: {DOCUMENT_LOADER_SETTINGS.Backend} | PERSIST: {DOCUMENT_LOADER_SETTINGS.Persist}")
        
    # -- Propiedades -- #
    @property
    def Logger(self):
        """
        Devuelve el logger del cargador de documentos.
        """
        return self.__logger