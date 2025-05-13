
# ---- MÓDULOS ---- #
import logging
from common.log.logger import get_logger

from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.converters import MultiFileConverter
from haystack.components.preprocessors import DocumentPreprocessor
from haystack.components.writers import DocumentWriter

from config.context import CONFIG

# ---- CLASES ---- #
class DocumentLoader:
    """
    
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        
        """
        self.__logger:logging.Logger = get_logger(__name__, file="app.log", console=False)
        self.__store:InMemoryDocumentStore = None
        
        if CONFIG.rag.backend == 'haystack':
            self.__store = InMemoryDocumentStore()
            self.__create_haystack_indexing_pipeline()
        
        self.__logger.info(f"DocumentLoader iniciado. BACKEND: {CONFIG.rag.backend} | PATH: {CONFIG.rag.docDirectory}")
    
    
    # -- Métodos privados -- #
    def __create_haystack_indexing_pipeline(self) -> None:
        """
        Crea la pipeline de indexación.
        """
        # Crea y añade los componentes del pipeline.
        self.__indexingPipeline:Pipeline = Pipeline()
        self.__indexingPipeline.add_component("converter", MultiFileConverter())
        self.__indexingPipeline.add_component("preprocessor", DocumentPreprocessor())
        self.__indexingPipeline.add_component("writer",
                                      DocumentWriter(document_store=self.__store))
        # Conecta los componentes entre ellos.
        self.__indexingPipeline.connect("converter", "preprocessor")
        self.__indexingPipeline.connect("preprocessor", "writer")
    # -- Métodos públicos -- #