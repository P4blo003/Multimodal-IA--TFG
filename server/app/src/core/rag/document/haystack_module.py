# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: haystack_module.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones base relaciondas con el módulo de RAG
    de documentos. Implementado mediante Haystack.
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
import os
from pathlib import Path
from typing import List
from contextlib import redirect_stdout, redirect_stderr
# Librerías externas
from haystack import Pipeline
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from haystack.components.converters import MultiFileConverter
from haystack.components.preprocessors import DocumentPreprocessor
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.writers import DocumentWriter
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
# Librerías internas
from .base import BaseDocumentModule
from model.context import ContextDTO
from utils.path import list_dir_files
from config.schema.rag import RagConfig


# ---- CLASES ---- #
class HaystackDocumentModule(BaseDocumentModule):
    """
    Clase base que representa un módulo de RAG. Contiene las funciones a implementar
    por los módulos de documentos. Implementado con Haystack
    """
    # -- Métodos por defecto -- #
    def __init__(self, rag_cfg:RagConfig):
        """
        Inicializa la instancia.
        
        Args:
            rag_cfg (RagConfig): Configuración del RAG.
        """
        # Inicializa las propiedades.
        self.__modelPath:Path = Path(os.path.join('.server', rag_cfg.installModelDir, rag_cfg.model.tag))
        self.__docPath:Path = Path(os.path.join('.server', rag_cfg.document.docDir))
        self.__store:QdrantDocumentStore = self.__crate_doc_store(rag_cfg=rag_cfg)
        self.__embeddingPipeline:Pipeline = self.__create_embedding_pipeline(rag_cfg=rag_cfg)
        self.__retrievePipeline:Pipeline = self.__create_retrieve_pipeline(rag_cfg=rag_cfg)
        
    # -- Métodos privados -- #
    def __crate_doc_store(self, rag_cfg:RagConfig) -> QdrantDocumentStore:
        """
        Crea y retorna un almacén de documentos.
        
        Args:
            rag_cfg (RagConfig): Configuración del RAG.
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            QdrantDocumentStore: Almacén de documentos de Qdrant.
        """
        # Try-Except para manejo de errores.
        try:
            # Retorna el almacén de documentos.
            return QdrantDocumentStore(
                path=os.path.join('.server', rag_cfg.document.storeDir, rag_cfg.document.framework),
                index='qdrantStorage',
                embedding_dim=rag_cfg.model.embeddingDim,
                recreate_index=True
            )
    
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"HaystackDocumentModule.__create_doc_store() -> [{type(e).__name__}] No se pudo crear el almacén de documentos. Trace: {e}")
    
    def __create_embedding_pipeline(self, rag_cfg:RagConfig) -> Pipeline:
        """
        Crea el pipeline para calcular los embeddings de documentos.
        
        Args:
            rag_cfg (RagConfig): Configuración del RAG.
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            Pipeline: Pipeline de embedding.
        """
        # Try-Except para manejo de errores.
        try:
            # Variable a retornar.
            pipeline:Pipeline = Pipeline()
            
            # Añade los componentes.
            pipeline.add_component(instance=MultiFileConverter(), name='converter')
            pipeline.add_component(instance=DocumentPreprocessor(split_by='word', split_length=rag_cfg.document.splitLength,
                                                                 split_overlap=rag_cfg.document.splitOverlap), name='preprocesor')
            pipeline.add_component(instance=SentenceTransformersDocumentEmbedder(str(self.__modelPath)), name='embedder')
            pipeline.add_component(instance=DocumentWriter(document_store=self.__store), name='writer')

            # Conecta los componentes.
            pipeline.connect("converter", "preprocesor")
            pipeline.connect("preprocesor", "embedder")
            pipeline.connect("embedder", "writer")
            
            # Retorna el pipeline.
            return pipeline
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"HaystackDocumentModule.__create_embedding_pipeline() -> [{type(e).__name__}] No se pudo crear el pipeline de embeddings. Trace: {e}")
    
    def __create_retrieve_pipeline(self, rag_cfg:RagConfig) -> Pipeline:
        """
        Crea el pipeline para obtenener el contexto relevante.
        
        Args:
            rag_cfg (RagConfig): Configuración del RAG.
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            Pipeline: Pipeline de recuperación.
        """
        # Try-Except para manejo de errores.
        try:
            # Variable a retornar.
            pipeline:Pipeline = Pipeline()
            
            # Añade los componentes.
            pipeline.add_component(instance=SentenceTransformersTextEmbedder(str(self.__modelPath)), name='embedder')
            pipeline.add_component(instance=QdrantEmbeddingRetriever(document_store=self.__store, top_k=rag_cfg.document.topK),
                                   name='retriever')

            # Conecta los componentes.
            pipeline.connect("embedder.embedding", "retriever.query_embedding")
            
            # Retorna el pipeline.
            return pipeline
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"HaystackDocumentModule.__create_retrieve_pipeline() -> [{type(e).__name__}] No se pudo crear el pipeline de recuperación. Trace: {e}")
    
    # -- Métodos BaseDocumentModule -- #
    def make_embeddings(self):
        """
        Calcula los embeddings de los documentos.
        
        Raises:
            OSError: En caso de que haya algún error.
        """
        # Try-Except para manejo de errores.
        try:
            # Obtiene los ficheros disponibles.
            filePaths:List[str] = list_dir_files(root_path=self.__docPath, recursive=True)
            
            # Imprime la información.
            print(f"Se disponen de {len(filePaths)} ficheros.")
            
            # Ejecuta el pipeline de embedding.
            with open(os.devnull, "w") as devnull:
                with redirect_stdout(devnull), redirect_stderr(devnull):
                    self.__embeddingPipeline.run({"converter": {"sources": filePaths}})
        
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excecpión.
            raise OSError(f"HaystackDocumentModule.make_embeddings() -> [{type(e).__name__}] No se pudo calcular los embeddings. Trace: {e}")
    
    def get_context(self, query:str):
        """
        Obtiene el contexto de la fuente de datos.
        
        Raises:
            OSError: En caso de que haya algún error.
        """
        # Try-Except para manejo de errores.
        try:
            # Obtiene los documentos más relevantes.
            with open(os.devnull, "w") as devnull:
                with redirect_stdout(devnull), redirect_stderr(devnull):
                    results = self.__retrievePipeline.run({"embedder" : {"text" : query}})
            
            # Variable a devolver.
            context:List[ContextDTO] = []
            
            # Para cada document obtenido.
            for doc in results['retriever']['documents']:
                # Añade el contexto.
                context.append(ContextDTO(score=doc.score, sourceType='Document', sourceDir=doc.meta['file_path'], content=doc.content))
            
            # Retorna el contexto.
            return context
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excecpión.
            raise OSError(f"HaystackDocumentModule.get_context() -> [{type(e).__name__}] No se pudo obtener el contexto. Trace: {e}")