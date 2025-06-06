# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/core/rag/haystack.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases relacionadas con el módulo RAG, implementado
# a partir del framwork de Haystack.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
from contextlib import redirect_stdout, redirect_stderr
from typing import List, Tuple

from .base import RagEngine
from config.schema import RagConfig
from utilities.system import list_dir
from utilities.system import create_path

# Haystack.
from haystack import Pipeline
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from haystack.components.converters import MultiFileConverter
from haystack.components.preprocessors import DocumentPreprocessor
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.writers import DocumentWriter
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever

# ---- CLASES ---- #
class HaystackEngine(RagEngine):
    """
    Clase que implementa los métodos de RagEngine. Implementa los métodos empleando el
    framework de Haystack.
    """
    # -- Métodos por defecto -- #
    def __init__(self, rag_cfg:RagConfig):
        """
        Inicializa la instancia.
        
        Args:
            rag_cfg (RagConfig): Configuración del rag.
        """
        # Establece las propiedades.
        self.__store:QdrantDocumentStore     = self.__create_store(rag_cfg=rag_cfg)                 # Almacén de embeddings.
        self.__embedPipeline:Pipeline        = self.__create_embed_pipeline(rag_cfg=rag_cfg)        # Pipeline de embeddings.
        self.__retrievalPipeline:Pipeline    = self.__create_retrieval_pipeline(rag_cfg=rag_cfg)    # Pipeline de recuperación.


    # -- Métodos privados -- #
    def __create_store(self, rag_cfg:RagConfig) -> QdrantDocumentStore:
        """
        Crea el almacen de los embeddings.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        
        Returns:
            QdrantDocumentStore: DocumentStore creada.
        """
        # Inicializa el almacén.
        return QdrantDocumentStore(
            path=create_path(rag_cfg.persistDir, rag_cfg.backend),
            index=rag_cfg.storeName,
            embedding_dim=rag_cfg.embeddingDim,
            recreate_index=True
        )

    def __create_embed_pipeline(self, rag_cfg:RagConfig) -> Pipeline:
        """
        Crea el pipeline de embedding.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        
        Returns:
            Pipeline: Pipeline de embedding.
        """
        # Inicializa el pipeline.
        pipeline = Pipeline()
        
        # Añade los componentes al pipeline.
        pipeline.add_component(instance=MultiFileConverter(), name="converter")
        pipeline.add_component(instance=DocumentPreprocessor(split_by="word", split_length=rag_cfg.splitLength, split_overlap=rag_cfg.splitOverlap), 
                                           name="preprocessor")
        pipeline.add_component(instance=SentenceTransformersDocumentEmbedder(create_path(rag_cfg.embedder.persistDir, rag_cfg.embedder.name)), name="embedder")
        pipeline.add_component(instance=DocumentWriter(document_store=self.__store), name="writer")

        # Conecta los componentes.
        pipeline.connect("converter", "preprocessor")
        pipeline.connect("preprocessor", "embedder")
        pipeline.connect("embedder", "writer")
        
        # Retorna el pipeline.
        return pipeline
    
    def __create_retrieval_pipeline(self, rag_cfg:RagConfig) -> Pipeline:
        """
        Crea el pipeline de recuperación.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        
        Returns:
            Pipeline: Pipeline de recuperación.
        """
        # Inicializa el pipeline.
        pipeline = Pipeline()
        
        # Añade los componentes.
        pipeline.add_component(instance=SentenceTransformersTextEmbedder(create_path(rag_cfg.embedder.persistDir, rag_cfg.embedder.name))
                                               , name="embedder")
        pipeline.add_component(instance=QdrantEmbeddingRetriever(document_store=self.__store, top_k=rag_cfg.topK)
                                               , name="retriever")
        
        # Conecta los componentes.
        pipeline.connect("embedder.embedding", "retriever.query_embedding")
        
        # Retorna el pipeline.
        return pipeline
    
    
    # -- Métodos RagEngine -- #
    def embed_data(self, rag_cfg:RagConfig) -> None:
        """
        Realiza el embedding de los datos.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        """
        # Obtiene los ficheros del directorio.
        filePaths:list[str] = list_dir(base_dir=rag_cfg.dataDir)
        
        # Ejecuta el pipeline de embedding.
        with open(os.devnull, "w") as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                self.__embedPipeline.run({"converter": {"sources": filePaths}})
    
    def get_relevant_context(self, query:str) -> List[Tuple[str, float]]:
        """
        Devuelve el contexto relevante obtenido a partir de almacén de embeddings.
        
        Args:
            query (str): Input del usuario. Necesario para obtener el contexto.
        
        Returns:
            List[Tuple[str,float]]: Listado con tuplas. Cada tupla contiene el score y contenido de un
                contexto relevante.
        """
        # Obtiene los documentos más relevantes.
        with open(os.devnull, "w") as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                results = self.__retrievalPipeline.run({"embedder" : {"text" : query}})

        # Obtiene el contenido y la puntuación-
        relevant_context: List[Tuple[str, float]] = [(doc.content, doc.score) for doc in results["retriever"]["documents"]]
        
        # Retorna el contexto relevante.
        return relevant_context