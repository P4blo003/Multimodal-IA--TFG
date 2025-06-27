# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: langchain_module.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones base relaciondas con el módulo de RAG
    de documentos. Implementado mediante LangChain.
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
import os
from pathlib import Path
from typing import List, TypedDict, Dict
from contextlib import redirect_stdout, redirect_stderr
# Librerías externas
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
# Librerías internas
from .base import BaseDocumentModule
from model.context import ContextDTO
from utils.path import list_dir_files
from config.schema.rag import RagConfig


# ---- CLASES ---- #
class State(TypedDict):
    """
    
    """
    # -- Atributos -- #
    question:str
    context:List[Document]
    answer:str

class LangChainDocumentModule(BaseDocumentModule):
    """
    Clase base que representa un módulo de RAG. Contiene las funciones a implementar
    por los módulos de documentos. Implementado con LangChain
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
        self.__storePath:Path = Path(os.path.join('.server', rag_cfg.document.storeDir, rag_cfg.document.framework))
        self.__docPath:Path = Path(os.path.join('.server', rag_cfg.document.docDir))
        
        self.__embedder:HuggingFaceEmbeddings = self.__create_embedder()
        self.__loader:DirectoryLoader = self.__create_loader()
        self.__splitter:RecursiveCharacterTextSplitter = self.__create_splitter(rag_cfg=rag_cfg)
        self.__qdrantClient:QdrantClient = self.__create_qdrant_client()
        self.__store:QdrantVectorStore = self.__create_store(rag_cfg=rag_cfg)
        
        self.__graph:CompiledStateGraph = self.__create_graph()
    
    # -- Métodos privados -- #
    def __create_embedder(self) -> HuggingFaceEmbeddings:
        """
        Crea y retorna el embedder.
        
        Args:
            rag_cfg: Configuración del RAG.
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            HuggingFaceEmbeddings: Embedder.
        """
        # Try-Except para manejo de errores.
        try:
            # Retorna el objeto.
            return HuggingFaceEmbeddings(model_name=str(self.__modelPath))

        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"LangChainDocumentModule.__create_embedder() -> [{type(e).__name__}] No se pudo crear el embedder. Trace: {e}")
    
    def __create_loader(self) -> DirectoryLoader:
        """
        Crea y retorna el cargador de documentos.
        
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            DirectoryLoader: Cargador de documentos.
        """
        # Try-Except para manejo de errores.
        try:
            # Retorna el objeto.
            return DirectoryLoader(self.__docPath)

        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"LangChainDocumentModule.__create_loader() -> [{type(e).__name__}] No se pudo crear el cargador de documentos. Trace: {e}")
    
    def __create_splitter(self, rag_cfg:RagConfig) -> RecursiveCharacterTextSplitter:
        """
        Crea y retorna el separador.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            RecursiveCharacterTextSplitter: Separador de documentos.
        """
        # Try-Except para manejo de errores.
        try:
            # Retorna el objeto.
            return RecursiveCharacterTextSplitter(chunk_size=rag_cfg.document.splitLength, chunk_overlap=rag_cfg.document.splitOverlap,
                                                  length_function=len, add_start_index=True)

        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"LangChainDocumentModule.__create_splitter() -> [{type(e).__name__}] No se pudo crear el separador de documentos. Trace: {e}")
    
    def __create_qdrant_client(self) -> QdrantClient:
        """
        Crea y retorna el cliente de Qdrant.
        
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            QdrantClient: Cliente de Qdrant.
        """
        # Try-Except para manejo de errores.
        try:
            # Retorna el objeto.
            return QdrantClient(path= self.__storePath)

        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"LangChainDocumentModule.__create_qdrant_client() -> [{type(e).__name__}] No se pudo crear el cliente de qdrant. Trace: {e}")

    def __create_store(self, rag_cfg:RagConfig) -> QdrantVectorStore:
        """
        Crea y retorna el almacén de Qdrant.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            QdrantVectorStore: Almacén de Qdrant.
        """
        # Try-Except para manejo de errores.
        try:
            # Comrpueba si la colección ya existe.
            if self.__qdrantClient.collection_exists(collection_name=rag_cfg.document.framework):
                # Obtiene la información.
                collection_info = self.__qdrantClient.get_collection(collection_name=rag_cfg.document.framework)
                
                # Comprueba si las dimensiones son diferentes.
                if collection_info.config.params.vectors.size != rag_cfg.model.embeddingDim:
                    # Recrea la colección.
                    self.__qdrantClient.recreate_collection(collection_name=rag_cfg.document.framework, 
                                                    vectors_config=VectorParams(size=rag_cfg.model.embeddingDim, distance=Distance.COSINE))

            # Si la colección no existe.
            else:
                # Crea la colección.
                self.__qdrantClient.create_collection(collection_name=rag_cfg.document.framework, 
                                                    vectors_config=VectorParams(size=rag_cfg.model.embeddingDim, distance=Distance.COSINE))
                
            # Retorna el objeto.
            return QdrantVectorStore(client=self.__qdrantClient, collection_name=rag_cfg.document.framework, embedding=self.__embedder)

        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"LangChainDocumentModule.__create_store() -> [{type(e).__name__}] No se pudo crear el almacén de documentos. Trace: {e}")
    
    def __retrieve(self, state:State) -> Dict:
        """
        Obtiene el contexto relevante. Función necesaria para poder usar grafos compilados.
        
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            Dict: Diccionario con el contexto.
        """
        # Try-Except para manejo de errores.
        try:
            # Obtiene los documentos relevantes y los retorna.
            return {"context":self.__store.similarity_search(state["question"])}
        
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"LangChainDocumentModule.__retrieve() -> [{type(e).__name__}] No se pudo obtener el contexto. Trace: {e}")
    
    def __create_graph(self) -> CompiledStateGraph:
        """
        Crea y retorna un stategraph compilado.
        
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            CompiledStateGraph
        """
        # Try-Except para manejo de errores.
        try:
            # Retorna el contexto relevante.
            graph_builder:StateGraph = StateGraph(State).add_node(self.__retrieve)
            graph_builder.add_edge(START, "__retrieve")
            # Retorna el graph.
            return graph_builder.compile()
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"LangChainDocumentModule.__create_graph() -> [{type(e).__name__}] No se pudo crear el graph. Trace: {e}")
      
    # -- Métodos BaseDocumentModule -- #
    def make_embeddings(self):
        """
        Calcula los embeddings de los documentos.
        
        Raises:
            OSError: En caso de que haya algún error.
        """
        # Try-Except para manejo de errores.
        try:
            # Obtiene los documentos y los separa.
            splits = self.__splitter.split_documents(self.__loader.load())
            
            # Añade los documentos al almacén.
            self.__store.add_documents(splits)
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"LangChainDocumentModule.make_embeddings() -> [{type(e).__name__}] No se pudo calcular los embeddings. Trace: {e}")
    
    def get_context(self, query):
        """
        Obtiene el contexto de la fuente de datos.
        
        Raises:
            OSError: En caso de que haya algún error.
        """
        # Try-Except para manejo de errores.
        try:
            # Variable a retornar.
            context:List[ContextDTO] = []
            
            # Procesa la respuesta.
            for doc in self.__graph.invoke({"question": query})['context']:
                # Añade el contexto.
                context.append(ContextDTO(score=0, sourceType='Document', sourceDir=doc.metadata['source'], content=doc.page_content))
            
            # Retorna el contexto.
            return context
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"LangChainDocumentModule.get_context() -> [{type(e).__name__}] No se pudo obtener el contexto. Trace: {e}")