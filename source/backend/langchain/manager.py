# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/backend/haystack/manager.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene las clases encargadas de gestionar el backend del 
# programa, como el sistema RAG o prompting, implementado con Langchain.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os

from backend.manager import BackendManager
from chat.history import ChatHistory

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from jinja2 import Template

from .prompt import create_prompt_template

from config.context import CFG


# ---- CLASES ---- #
class LangChainManager(BackendManager):
    """
    Instancia que extiende `BackendManager` y se configura para emplear el módulo de
    `LangChain`.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la instancia.
        """
        super().__init__()      # Constructor de BackendManager.
        # Inicializa las propiedades.
        self.__embeddingModel:HuggingFaceEmbeddings = HuggingFaceEmbeddings(model_name=os.path.join(CFG.rag.embedding.persistDirectory, CFG.rag.embedding.model))
        self.__qdrantClient:QdrantClient = QdrantClient(path=os.path.join(CFG.rag.embedding.persistDirectory, CFG.rag.embedding.model))
        self.__qdrantClient.recreate_collection(
            collection_name="Document",
            vectors_config=VectorParams(
                size=CFG.rag.embeddingDim,
                distance=Distance.COSINE
            )
        )       # Crea la colección en Qdrant.
        self.__vectoreSotore:QdrantVectorStore = QdrantVectorStore(
            client=self.__qdrantClient,
            collection_name="Document",
            embedding=self.__embeddingModel
        )
        self.__promptTemplate:Template = create_prompt_template(file_path=CFG.prompt.templateFile)  # Crea el prompt template.
        self.EmbedDocuments()                   # Realiza el embedding de los documentos.
        
        self.Logger.info("Backend iniciado. TYPE: LangChain")    # Imprime información.
        
    # -- Métodos BackendManager -- #
    def EmbedDocuments(self) -> list:
        """
        Realiza el embedding de los documentos.
        """        
        # Obtiene los documentos del directorio.
        __loader:DirectoryLoader = DirectoryLoader(CFG.rag.docDirectory)
        __documents = __loader.load()
        
        # Procesa los documentos.
        __splitter:RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=CFG.rag.splitLength,
            chunk_overlap=CFG.rag.splitOverlap,
            length_function=len,
            add_start_index=True
        )
        __chunks = __splitter.split_documents(__documents)
        
        # Añade los documentos al almacén de vectores.
        self.__vectoreSotore.add_documents(__chunks)
                
    # -- Métodos BackendManager -- #
    def BuildPrompt(self, user_input:str, history:ChatHistory) -> str:
        """
        Construye el prompt a partir del contexto, historial y query.
        
        Args:
            user_input (str): Input del usuario.
            history (ChatHistory): Historial del chat.
            
        Returns:
            str: El prompt construido.
        """
        # Obtiene los documentos más relevantes.
        __results = self.__vectoreSotore.similarity_search_with_relevance_scores(user_input, k=CFG.rag.topK)
        
        # Obtiene solo el contenido de los documentos.
        __content:list = []
        for __doc, __ in __results:
            __content.append(__doc.page_content)
            
        return self.__promptTemplate.render(context=__content, history=history.GetHistory(), user_input=user_input)