
# ---- MÓDULOS ---- #
import os
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr

from chat.history import ChatHistory

from backend.manager import BackendManager
from .components import create_prompt_builder

from haystack import Pipeline
from haystack.components.converters import MultiFileConverter
from haystack.components.preprocessors import DocumentPreprocessor
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.writers import DocumentWriter
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore

from config.context import CFG


# ---- CLASES ---- #
class HaystackManager(BackendManager):
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
            path=CFG.rag.persistDirectory,
            index="Document",
            embedding_dim=CFG.rag.embeddingDim,
            recreate_index=False
        )
        self.__embedPipeline:Pipeline = Pipeline()
        self.__retrievePipeline:Pipeline = Pipeline()
        self.__promptBuilder:PromptBuilder = create_prompt_builder(file_path=CFG.prompt.templateFile, variables=CFG.prompt.variables)
        self.__create_embed_pipeline()      # Inicializa el pipeline.
        self.__create_retrieve_pipeline()   # Inicializa el pipelin.
        
        self.EmbedDocuments()               # Realiza el embedding de los documentos.
        self.Logger.info("Backend iniciado. TYPE: Haystack")    # Imprime información.

    # -- Métodos privados -- #
    def __create_embed_pipeline(self) -> any:
        """
        Crea e inicializa el pipeline de embedding.
        """
        # Inicializa los componentes.
        __converter:MultiFileConverter = MultiFileConverter()
        __preprocessor:DocumentPreprocessor = DocumentPreprocessor()
        __embedder:SentenceTransformersDocumentEmbedder = SentenceTransformersDocumentEmbedder(os.path.join(CFG.rag.embeddingModelDirectory, CFG.rag.embeddingModel))
        __writer:DocumentWriter = DocumentWriter(document_store=self.__docStore)
        
        # Añade los componentes.
        self.__embedPipeline.add_component("converter", __converter)
        self.__embedPipeline.add_component("preprocessor", __preprocessor)
        self.__embedPipeline.add_component("embedder", __embedder)
        self.__embedPipeline.add_component("writer", __writer)
        
        # Conecta los componentes.
        self.__embedPipeline.connect("converter", "preprocessor")
        self.__embedPipeline.connect("preprocessor", "embedder")
        self.__embedPipeline.connect("embedder", "writer")
    
    def __create_retrieve_pipeline(self) -> any:
        """
        Crea e inicializa el pipeline de recuperación.
        """
        # Inicializa los componentes.
        __embedder:SentenceTransformersTextEmbedder = SentenceTransformersTextEmbedder(os.path.join(CFG.rag.embeddingModelDirectory, CFG.rag.embeddingModel))
        __retriever:QdrantEmbeddingRetriever = QdrantEmbeddingRetriever(document_store=self.__docStore)
        
        # Añade los componentes.
        self.__retrievePipeline.add_component("embedder", __embedder)
        self.__retrievePipeline.add_component("retriever", __retriever)

        # Conecta los componentes.
        self.__retrievePipeline.connect("embedder.embedding", "retriever.query_embedding")
        
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
        with open(os.devnull, "w") as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                results = self.__retrievePipeline.run({"embedder" : {"text" : user_input}})
                
        __topDocs = results["retriever"]["documents"][:CFG.rag.topKDocs]    # Obtiene los topKDocs mejores documentos.
        
        # Devuelve el prompt generado.
        return self.__promptBuilder.run(context=__topDocs, history=history.GetHistory(), user_input=user_input)["prompt"]

    # -- Métodos públicos -- #
    def EmbedDocuments(self) -> any:
        """
        Realiza el embedding de los documentos.
        """
        # Obtiene una lista con los ficheros de los documentos.
        __filePaths = [str(path) for path in Path(CFG.rag.docDirectory).rglob("*") if path.is_file()]
        
        # Ejecuta el pipeline.
        with open(os.devnull, "w") as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                self.__embedPipeline.run({"converter": {"sources": __filePaths}})
        self.Logger.info(f"Embedding de documentos realizado. PATH: {CFG.rag.docDirectory}")    # Imprime información.