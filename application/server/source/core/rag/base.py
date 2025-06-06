# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/core/rag/base.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases base relacionadas con el RAG.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from abc import ABC
from abc import abstractmethod
from yaspin import yaspin

from core.hugging_face import HuggingFaceService

from config.schema import RagConfig, EmbedderConfig


# ---- CLASES ---- #
class RagEngine(ABC):
    """
    Clase base. Especifica los métodos que deberán implementar las clases que hereden de
    esta. Se encarga de los embeddings de los datos y la recuperación de los mismos.
    """
    # -- Métodos abstractos -- #
    @abstractmethod
    def embed_data(self) -> None:
        """
        Realiza el embedding de los datos.
        """
        pass
    
    @abstractmethod
    def get_relevant_context(self, query:str):
        """
        Devuelve el contexto relevante obtenido a partir de almacén de embeddings.
        
        Args:
            query (str): Input del usuario. Necesario para obtener el contexto.
        """
        pass
    
    # -- Métodos públicos -- #
    def check_embed_model(self, model_cfg:EmbedderConfig) -> None:
        """
        Comprueba si el modelo esta instalado. En caso de que no lo este, lo instala.
        
        Args:
            model_cfg (EmbedderConfig): Configuración del modelo de embeddings.
        """
        
        # Comprueba si el modelo esta instalado.
        if not HuggingFaceService.model_installed(model_name=model_cfg.name, dir=model_cfg.persistDir):
            with yaspin(text=f"Instalando modelo {model_cfg.name}...") as sp:
                # Instala el modelo.
                HuggingFaceService.install_model(model_name=model_cfg.name, dir=model_cfg.persistDir)