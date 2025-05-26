
# ---- MÓDULOS ---- #
import os
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr

from chat.history import ChatHistory

from backend.manager import BackendManager

from common.system import list_all_files

from .components import create_prompt_builder

from haystack import Pipeline
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from haystack.components.converters import MultiFileConverter
from haystack.components.preprocessors import DocumentPreprocessor
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.writers import DocumentWriter
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever

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
            path=os.path.join(CFG.rag.persistDirectory, CFG.rag.backend),
            index="Document",
            embedding_dim=CFG.rag.haystack.embeddingDim,
            recreate_index=True
        )
        self.__embedPipeline:Pipeline = Pipeline()
        self.__init_embed_pipeline()            # Inicializa el pipeline.
        self.__retrievePipeline:Pipeline = Pipeline()
        self.__init_retrive_pipelin()           # Inicializa el pipeline.
        self.__promptBuilder:PromptBuilder = create_prompt_builder(file_path=CFG.prompt.templateFile, variables=CFG.prompt.variables)
        
        self.EmbedDocuments()                   # Realiza el embedding de los documentos.
        self.Logger.info("Backend iniciado. TYPE: Haystack")    # Imprime información.
    
    # -- Métodos privados -- #
    def __init_embed_pipeline(self) -> any:
        """
        Crea e inicializa el pipeline de embedding.
        """
        # Inicializa los componentes.
        __converter:MultiFileConverter = MultiFileConverter()
        __preprocessor:DocumentPreprocessor = DocumentPreprocessor(split_by="word", split_length=CFG.rag.splitLength, split_overlap=CFG.rag.splitOverlap)
        __embedder:SentenceTransformersDocumentEmbedder = SentenceTransformersDocumentEmbedder(os.path.join(CFG.rag.embedding.persistDirectory, CFG.rag.embedding.model))
        __writer:DocumentWriter = DocumentWriter(document_store=self.__docStore)
        
        # Añade los componentes al pipeline.
        self.__embedPipeline.add_component(instance=__converter, name="converter")
        self.__embedPipeline.add_component(instance=__preprocessor, name="preprocessor")
        self.__embedPipeline.add_component(instance=__embedder, name="embedder")
        self.__embedPipeline.add_component(instance=__writer, name="writer")
        
        # Conecta los componentes.
        self.__embedPipeline.connect("converter", "preprocessor")
        self.__embedPipeline.connect("preprocessor", "embedder")
        self.__embedPipeline.connect("embedder", "writer")
        
    def __init_retrive_pipelin(self) -> any:
        """
        Crea e inicializa el pipeline de recuperación.
        """
        # Inicializa los componentes.
        __embedder:SentenceTransformersTextEmbedder = SentenceTransformersTextEmbedder(os.path.join(CFG.rag.embedding.persistDirectory, CFG.rag.embedding.model))
        __retriever:QdrantEmbeddingRetriever = QdrantEmbeddingRetriever(document_store=self.__docStore, top_k=CFG.rag.topK)
        __promptBuilder:PromptBuilder = create_prompt_builder(file_path=CFG.prompt.templateFile, variables=CFG.prompt.variables)
        
        # Añade los componentes al pipeline.
        self.__retrievePipeline.add_component(instance=__embedder, name="embedder")
        self.__retrievePipeline.add_component(instance=__retriever, name="retriever")
        
        # Conecta los componentes.
        self.__retrievePipeline.connect("embedder.embedding", "retriever.query_embedding")
    
    # -- Métodos BackendManager -- #
    def EmbedDocuments(self) -> any:
        """
        Realiza el embedding de los documentos.
        """
        # Obtiene los ficheros del directorio.
        __filePaths:list[str] = list_all_files(base_dir=CFG.rag.docDirectory)
        
        # Ejecuta el pipeline de embedding.
        with open(os.devnull, "w") as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                self.__embedPipeline.run({"converter": {"sources": __filePaths}})
        self.Logger.info("Realizado embedding de documentos.")      # Imprime información.

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
                __results = self.__retrievePipeline.run({"embedder" : {"text" : user_input}})
        
        # Obtiene solo el contenido del 
        __content:list = []
        for __doc in __results["retriever"]["documents"]:
            __content.append(__doc.content)
        
        # Devuelve el prompt generado.
        return self.__promptBuilder.run(context=__content, history=history.GetHistory(), user_input=user_input)["prompt"]