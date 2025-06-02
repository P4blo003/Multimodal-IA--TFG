
# ---- MÓDULOS ----- #
import os
from abc import ABC
from utils.system import list_all_files
from contextlib import redirect_stdout, redirect_stderr
from abc import abstractmethod

from logging import Logger
from utils.logger import create_logger
from utils.model import model_installed, install_model

from core.session import ChatSession

from haystack import Pipeline
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from haystack.components.converters import MultiFileConverter
from haystack.components.preprocessors import DocumentPreprocessor
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.writers import DocumentWriter
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from .haystack import create_prompt_builder

from config.context import CFG


# ---- CLASES ---- #
class BaseBackend(ABC):
    """
    Instancia base que se encarga de manejar todo lo relacionado con el backend del sistema.
    Se encarga de gestionar el RAG y prompting.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la instancia.
        """
        # Inicializa las propiedades.
        self.__logger:Logger = create_logger(logger_name=__name__, cfg=CFG.logger, console=False, file="server.log")
        self.__check_embedding_model()
    
    
    # -- Propiedades -- #
    @property
    def Logger(self) -> Logger:
        """
        Devuelve el logger del manager.
        
        Returns:
            Logger: El logger del manager.
        """
        return self.__logger
    
    
    # -- Métodos públicos -- #
    def __check_embedding_model(self) -> None:
        """
        Comprueba si el modelo de embedding esta instalado y en caso de que no lo esté,
        lo instala.
        """
        # Comprueba si el modelo está instalado.
        if not model_installed(model_name=CFG.rag.embedding.model, json_path=CFG.rag.embedding.file):
            
            self.Logger.warning(f"El modelo {CFG.rag.embedding.model} no esta instalado. Instalando ...")       # Imprime la información.
            path:str = install_model(model_name=CFG.rag.embedding.model, json_path=CFG.rag.embedding.file, dir=CFG.rag.embedding.persistDirectory) # Instala el modelo.
            self.Logger.info(f"Modelo {CFG.rag.embedding.model} instalado. PATH: {path}")                       # Imprime la información.
    

    # -- Métodos abstractos -- # 
    @abstractmethod
    def EmbedDocuments(self) -> None:
        """
        Realiza el embedding de los documentos.
        """   
        pass

    @abstractmethod
    def BuildPrompt(self, user_input:str, session:ChatSession) -> str:
        """
        Construye el prompt a partir del contexto, historial y query.
        
        Args:
            user_input (str): Input del usuario.
            session (ChatSession): Sesión del chat.
            
        Returns:
            str: El prompt construido.
        """
        pass


class HaystackBackend(BaseBackend):
    """
    Instancia que extiende `BackendManager` y se configura para emplear el módulo de
    `Haystack`.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la instancia.
        """
        super().__init__()      # Constructor de BackendManager.
        # Inicializa las propiedades.
        self.__docStore:QdrantDocumentStore = QdrantDocumentStore(
            path=os.path.join(CFG.rag.persistDirectory, CFG.rag.backend),
            index="Document",
            embedding_dim=CFG.rag.embeddingDim,
            recreate_index=True
        )
        self.__embedPipeline:Pipeline = Pipeline()
        self.__init_embed_pipeline()                # Inicializa el pipeline.
        self.__retrievePipeline:Pipeline = Pipeline()
        self.__init_retrive_pipeline()              # Inicializa el pipeline.
        self.__promptBuilder:PromptBuilder = create_prompt_builder(file_path=CFG.prompt.templateFile, variables=CFG.prompt.variables)
        
        self.EmbedDocuments()                       # Realiza el embedding de los documentos.
        self.Logger.info("Backend iniciado. TYPE: Haystack")    # Imprime información.
    
    
    # -- Métodos privados -- #
    def __init_embed_pipeline(self) -> any:
        """
        Crea e inicializa el pipeline de embedding.
        """
        # Inicializa los componentes.
        converter:MultiFileConverter = MultiFileConverter()
        preprocessor:DocumentPreprocessor = DocumentPreprocessor(split_by="word", split_length=CFG.rag.splitLength, split_overlap=CFG.rag.splitOverlap)
        embedder:SentenceTransformersDocumentEmbedder = SentenceTransformersDocumentEmbedder(os.path.join(CFG.rag.embedding.persistDirectory, CFG.rag.embedding.model))
        writer:DocumentWriter = DocumentWriter(document_store=self.__docStore)
        
        # Añade los componentes al pipeline.
        self.__embedPipeline.add_component(instance=converter, name="converter")
        self.__embedPipeline.add_component(instance=preprocessor, name="preprocessor")
        self.__embedPipeline.add_component(instance=embedder, name="embedder")
        self.__embedPipeline.add_component(instance=writer, name="writer")
        
        # Conecta los componentes.
        self.__embedPipeline.connect("converter", "preprocessor")
        self.__embedPipeline.connect("preprocessor", "embedder")
        self.__embedPipeline.connect("embedder", "writer")
        
    def __init_retrive_pipeline(self) -> any:
        """
        Crea e inicializa el pipeline de recuperación.
        """
        # Inicializa los componentes.
        embedder:SentenceTransformersTextEmbedder = SentenceTransformersTextEmbedder(os.path.join(CFG.rag.embedding.persistDirectory, CFG.rag.embedding.model))
        retriever:QdrantEmbeddingRetriever = QdrantEmbeddingRetriever(document_store=self.__docStore, top_k=CFG.rag.topK)
        
        # Añade los componentes al pipeline.
        self.__retrievePipeline.add_component(instance=embedder, name="embedder")
        self.__retrievePipeline.add_component(instance=retriever, name="retriever")
        
        # Conecta los componentes.
        self.__retrievePipeline.connect("embedder.embedding", "retriever.query_embedding")
    
    
    # -- Métodos BaseBackend -- #
    def EmbedDocuments(self) -> None:
        """
        Realiza el embedding de los documentos.
        """
        # Obtiene los ficheros del directorio.
        filePaths:list[str] = list_all_files(base_dir=CFG.rag.docDirectory)
        
        # Ejecuta el pipeline de embedding.
        with open(os.devnull, "w") as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                self.__embedPipeline.run({"converter": {"sources": filePaths}})
        self.Logger.info("Realizado embedding de documentos.")      # Imprime información.
    
    def BuildPrompt(self, user_input:str, session:ChatSession) -> str:
        """
        Construye el prompt a partir del contexto, historial y query.
        
        Args:
            user_input (str): Input del usuario.
            session (ChatSession): Sesión del chat.
            
        Returns:
            str: El prompt construido.
        """
        # Obtiene los documentos más relevantes.
        with open(os.devnull, "w") as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                __results = self.__retrievePipeline.run({"embedder" : {"text" : user_input}})
        
        # Obtiene solo el contenido de los documentos.
        __content:list = []
        for __doc in __results["retriever"]["documents"]:
            __content.append(__doc.content)
        
        # Devuelve el prompt generado.
        return self.__promptBuilder.run(context=__content, history=session.get_history(), user_input=user_input)["prompt"]
    

class LangChainBackend(BaseBackend):
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
    
    
    # -- Métodos BaseBackend -- #
    def EmbedDocuments(self) -> None:
        """
        Realiza el embedding de los documentos.
        """
        pass
    
    def BuildPrompt(self, user_input:str, session:ChatSession) -> str:
        """
        Construye el prompt a partir del contexto, historial y query.
        
        Args:
            user_input (str): Input del usuario.
            session (ChatSession): Sesión del chat.
            
        Returns:
            str: El prompt construido.
        """
        pass