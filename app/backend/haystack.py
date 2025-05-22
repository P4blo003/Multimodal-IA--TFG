# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/backend/haystack.py
# Autor: Pablo González García
# Descripción: 

# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
from pathlib import Path

from .base import LAMBackend

from haystack import Pipeline
from haystack.components.converters import MultiFileConverter
from haystack.components.preprocessors import DocumentPreprocessor
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore

from config.context import CONFIG


# ---- CLASES ---- #
class HaystackBackend(LAMBackend):
    """
    Esta clase representa el backend de haystack. Implementa las funciones necesarias para
    hacer consultas al modelo empleando haystack.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la clase.
        """
        super().__init__()  # Constructor de LAMBackend.
        # Inicializa los parámetros.
        self.__docStore:InMemoryDocumentStore = InMemoryDocumentStore()
        self.__indexingPipeline:Pipeline = Pipeline()          # Pipeline de componentes.
        self.__createIndexingPipeline()                         # Inicializa el pipeline.
        
        self.Logger.info("Backend iniciado. TYPE: Haystack")   # Imprime información.
    
    # -- Propiedades -- #
    @property
    def DocStore(self) -> InMemoryDocumentStore:
        """
        Devuelve el almacén de documentos.
        
        Returns:
            InMemoryDocumentStore: El almacén de documentos.
        """
        return self.__docStore
    @property
    def IndexingPipeline(self) -> Pipeline:
        """
        Devuelve el pipeline de indexación.
        
        Returns:
            Pipeline: El pipeline de indexación.
        """
    
    # -- Métodos privados -- #
    def __createIndexingPipeline(self):
        """
        Crea e inicializa el pipeline de indexación.
        """
        # Inicializa los componentes.
        converter:MultiFileConverter = MultiFileConverter()
        preprocessor:DocumentPreprocessor = DocumentPreprocessor()
        path:str = os.path.join(CONFIG.rag.modelDirectory, CONFIG.rag.embeddingModel)
        embedder:SentenceTransformersDocumentEmbedder = SentenceTransformersDocumentEmbedder(model={path})
        writer = DocumentWriter(document_store=self.__docStore)
        # Añade los componetnes.
        self.__indexingPipeline.add_component("converter", converter)
        self.__indexingPipeline.add_component("preprocessor", preprocessor)
        self.__indexingPipeline.add_component("embedder", embedder)
        self.__indexingPipeline.add_component("writer", writer)
        # Conecta los componentes.
        self.__indexingPipeline.connect("converter", "preprocessor")
        self.__indexingPipeline.connect("preprocessor", "embedder")
        self.__indexingPipeline.connect("embedder", "writer")    
    
    # -- Métodos abstractos -- #
    def IndexDocuments(self):
        """
        Indexa los documentos.
        """
        dir_path:Path = Path(CONFIG.rag.docDirectory)
        file_paths:list = [str(file) for file in dir_path.iterdir() if file.is_file()]
        self.__indexingPipeline.run({"converter": {"sources": file_paths}})