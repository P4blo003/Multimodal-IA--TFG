# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/core/rag/factory.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases relacionadas con la creación de componentes
# relacionados con el módulo RAG.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from .base import RagEngine
from .haystack import HaystackEngine
from .langchain import LangChainEngine

from config.schema import RagConfig


# ---- CLASES ---- #
class EngineFactory:
    """
    Clase que se encarga de la creación de los engine de RAG.
    """
    # -- Métodos estáticos -- #
    @staticmethod
    def create_engine(rag_cfg:RagConfig) -> RagEngine:
        """
        Crea y retorna un RagEngine en función del tipo dado.
        
        Args:
            rag_cfg (RagConfig): Congiguración del RAG.
        
        Returns:
            RagEngine: Instancia RagEngine.
        """
        # Retorna el RagEngine.
        match(rag_cfg.backend):
            # Si es para Haystack.
            case 'HAYSTACK':
                return HaystackEngine(rag_cfg=rag_cfg)

            # Si es para LangChain.
            case 'LANGCHAIN':
                return LangChainEngine(rag_cfg=rag_cfg)