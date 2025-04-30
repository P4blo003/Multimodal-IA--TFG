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

from utils.logger import get_logger

# Dependencias de Haystack
from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore as HSInMemStore
from haystack.components.converters import MultiFileConverter
from haystack.components.preprocessors import DocumentPreprocessor, DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter

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
        self.__validExtensions:list[str] = cfg.get('documents', {}).get('valid_extensions', [".pdf", ".docx", ".txt", ".csv", ".xlsx"])
        match self.__backend:
            case 'haystack':
                self.__store = HSInMemStore()
                self.__create_haystack_pipeline()
                self.__logger.info("Iniciado DocumentStore de Haystack.")
            case 'langchain':
                self.__store = []
                self.__logger.info("Iniciado DocumentStore de LangChain.")

    # Métodos privados #
    def __create_haystack_pipeline(self):
        """
        Crea una pipeline de Haystack con conversión, preprocesamiento e indexación.
        """
        self.__pipeline = Pipeline()
        self.__pipeline.add_component("converter", MultiFileConverter())
        self.__pipeline.add_component("preprocessor", DocumentPreprocessor())
        self.__pipeline.add_component("writer", DocumentWriter(document_store=self.__store))
        self.__pipeline.connect("converter", "preprocessor")
        self.__pipeline.connect("preprocessor", "writer")
    
    def __load_with_haystack(self):
        """
        Flujo completo de ingesta y preprocesamiento usando Haysatck:
        - Conversión de múltiples formatos a documentos.
        - Limpieza semántica.
        - Segmentación configurable.
        - Indezación en InMemoryDocuemntStore.
        """
        files = [os.path.join(self.__docDir, file) for file in os.listdir(self.__docDir)
                 if os.path.splitext(file)[1].lower() in self.__validExtensions]
        
        # Si no hay archivos para procesar.
        if not files:
            self.__logger.warning("No se encontraron archivos válidos para procesar.")
            return
        
        try:
            result = self.__pipeline.run(data={"sources": files})
            self.__logger.info(f"Pipeline de Haystack ejecutada correctamente: {len(files)}")
        except Exception as ex:
            self.__logger.exception(f"Error ejecutando la pipeline de Haystack: {ex}")

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
                self.__load_with_haystack()
            case 'langchain':
                pass