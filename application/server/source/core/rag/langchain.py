# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/core/rag/langchain.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases relacionadas con el módulo RAG, implementado
# a partir del framwork de LangChain.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from typing import List, Tuple

from .base import RagEngine
from config.schema import RagConfig
from utilities.system import create_path

# LangChain.
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


# ---- CLASES ---- #
class LangChainEngine(RagEngine):
    """
    Clase que implementa los métodos de RagEngine. Implementa los métodos empleando el
    framework de LangChain.
    """
    # -- Métodos por defecto -- #
    def __init__(self, rag_cfg:RagConfig):
        """
        Inicializa la instancia.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        """
        # Establece las propiedades.
        self.__embedder:HuggingFaceEmbeddings = self.__create_embedder(rag_cfg=rag_cfg)
        self.__loader:DirectoryLoader = self.__create_loader(rag_cfg=rag_cfg)
        self.__splitter:RecursiveCharacterTextSplitter = self.__create_splitter(rag_cfg=rag_cfg)
        self.__qdrantClient:QdrantClient = self.__create_qdrant_client(rag_cfg=rag_cfg)
        self.__store:QdrantVectorStore = None
        
    
    # -- Métodos privados -- #
    def __create_embedder(self, rag_cfg:RagConfig) -> HuggingFaceEmbeddings:
        """
        Inicializa el modelo de embedding.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        
        Returns:
            HuggingFaceEmbeddings: Embedder de hugging face.
        """
        # Crea la ruta del modelo.
        model_path:str = create_path(rag_cfg.persistDir, rag_cfg.embedder.name)
        
        # Crea el embedder.
        return HuggingFaceEmbeddings(model_path)
    
    def __create_loader(self, rag_cfg:RagConfig) -> DirectoryLoader:
        """
        Inicializa el cargador.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        
        Returns:
            DirectoryLoader: Cargador del directorio.
        """
        # Crea el cargador de documentos.
        return DirectoryLoader(rag_cfg.dataDir)
    
    def __create_splitter(self, rag_cfg:RagConfig) -> RecursiveCharacterTextSplitter:
        """
        Inicializa el separador.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        
        Returns:
            RecursiveCharacterTextSplitter: Separador de documentos.
        """
        return RecursiveCharacterTextSplitter(chunk_size=rag_cfg.splitLength, chunk_overlap=rag_cfg.splitOverlap,
            length_function=len, add_start_index=True)
    
    def __create_qdrant_client(self, rag_cfg:RagConfig) -> QdrantClient:
        """
        Inicializa el cliente de Qdrant.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        
        Returns:
            QdrantClient: Cliente de Qdrant.
        """
        return QdrantClient(path= create_path(rag_cfg.persistDir, rag_cfg.backend), prefer_grpc=True)
    
    def __create_qdrant_store(self, rag_cfg:RagConfig) -> QdrantVectorStore:
        """
        Inicializa el almacén de Qdrant.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        
        Returns:
            QdrantVectorStore: Almacén de Qdrant.
        """
        # Comrpueba si la colección ya existe.
        if self.__qdrantClient.collection_exists(collection_name=rag_cfg.storeName):
            # Obtiene la información.
            collection_info = self.__qdrantClient.get_collection(collection_name=rag_cfg.storeName)
            # Comprueba si las dimensiones son diferentes.
            if collection_info.config.params.vectors.size != rag_cfg.embeddingDim:
                # Recrea la colección.
                self.__qdrantClient.recreate_collection(collection_name=rag_cfg.storeName, 
                                                  vectors_config=VectorParams(size=rag_cfg.embeddingDim, distance=Distance.COSINE))

        # Si la colección no existe.
        else:
            # Crea la colección.
            self.__qdrantClient.create_collection(collection_name=rag_cfg.storeName, 
                                                  vectors_config=VectorParams(size=rag_cfg.embeddingDim, distance=Distance.COSINE))
        
        # Retorna el almacén.
        return QdrantVectorStore(client=self.__qdrantClient, collection_name=rag_cfg.storeName, embedding=self.__embedder)

        
    # -- Métodos RagEngine -- #
    def embed_data(self, rag_cfg:RagConfig) -> None:
        """
        Realiza el embedding de los datos.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
        """
        pass
    
    def get_relevant_context(self, query:str) -> List[Tuple[str, float]]:
        """
        Devuelve el contexto relevante obtenido a partir de almacén de embeddings.
        
        Args:
            query (str): Input del usuario. Necesario para obtener el contexto.
        
        Returns:
            List[Tuple[str,float]]: Listado con tuplas. Cada tupla contiene el score y contenido de un
                contexto relevante.
        """
        # Obtiene los documentos y preprocesa los documentos.
        documents = self.__loader.load()
        chunks = self.__splitter.split_documents(documents=documents)
        self.__store.add_documents(chunks)