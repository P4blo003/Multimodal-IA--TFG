# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/core/conversation.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene la clase realacionada con la gestión de la
# conversación.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from typing import List, Tuple
from .session import ChatSession
from .rag.base import RagEngine
from .rag.factory import EngineFactory
from .prompt import PromptBuilder
from .ollama import OllamaService

from logging import Logger
from utilities.logger import create_logger

from config.schema import RagConfig, OllamaAPIConfig, LoggerConfig


# ---- CLASES ---- #
class ConversationController:
    """
    Clase encargada de gestionar la conversación. Gestiona la obtención de contexto, historial
    y generación de la respuesta.
    """
    # -- Métodos por defecto -- #
    def __init__(self, rag_cfg:RagConfig, promp_cfg:PromptBuilder, logger_cfg:LoggerConfig):
        """
        Inicializa la instancia.
        
        Args:
            rag_cfg (RagConfig): Configuración del Rag.
            prompt_cfg (PromptConfig): Configuración del prompt.
            logger_cfg (LoggerConfig): Configuración del logger.
        """
        # Inicializa las propiedades.
        self.__logger:Logger = create_logger(logger_name=__name__, cfg=logger_cfg, console=True, file='server.log')
        self.__ragEngine:RagEngine = EngineFactory.create_engine(rag_cfg=rag_cfg)
        self.__promptBuilder:PromptBuilder = PromptBuilder(prompt_cfg=promp_cfg)
        self.__ragEngine.check_embed_model(model_cfg=rag_cfg.embedder)      # Comprueba si el modelo está instalado.
        self.__ragEngine.embed_data(rag_cfg=rag_cfg)                        # Realiza los embeddings.

        self.__logger.info("Controlador de conversación iniciado.")         # Imprime la información.


    # -- Métodos públicos -- #
    def chat(self, query:str, chat_session:ChatSession, ollama_api_cfg:OllamaAPIConfig) -> str:
        """
        Genera el prompt a partir de la query, contexto del RAG e historial, envía la petición
        a la API de Ollama y recibe la respuesta.
        
        Args:
            query (str): Query realizada por el usuario.
            chat_session (ChatSession): Sesión de chat que contiene el historial.
            ollama_api_cfg (OllamaAPIConfig): Configuración de la API de Ollama.
        
        Returns:
            str: Respuesta generada por el modelo.
        """
        # Obtiene el contexto relevante.
        context:List[Tuple[str, float]] = self.__ragEngine.get_relevant_context(query=query)
        
        # Genera el prompt.
        prompt:str = self.__promptBuilder.create_prompt(context=context, chat_history=chat_session.ChatHistory, query=query)
        
        # Retorna la respuesta generada por el modelo.
        return OllamaService.get_response(prompt=prompt, host=ollama_api_cfg.host, port=ollama_api_cfg.port, model_name=ollama_api_cfg.model.name)