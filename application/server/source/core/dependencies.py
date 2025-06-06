# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/core/dependencies.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las dependencias del programa. Contiene funciones
# para obtener sus valores desde diferentes partes del código.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from core.session import SessionController
from core.conversation import ConversationController
from core.ollama import OllamaController

from config.context import CFG


# ---- PARÁMETROS ---- #
__session_controller:SessionController = SessionController(logger_cfg=CFG.logger)
__conversation_controller:ConversationController = ConversationController(rag_cfg=CFG.rag, promp_cfg=CFG.prompt, logger_cfg=CFG.logger)
__ollama_controller:OllamaController = OllamaController(logger_cfg=CFG.logger)


# ---- FUNCIONES ---- #
def get_session_controller() -> SessionController:
    """
    Retorna a instancia del controlador de sesión.
    
    Returns:
        SessionController: Controlador de la sesión.
    """
    # Retorna el controlador.
    return __session_controller

def get_conversation_controller() -> ConversationController:
    """
    Retorna a instancia del controlador de conversación.
    
    Returns:
        ConversationController: Controlador de la conversación.
    """
    # Retorna el controlador.
    return __conversation_controller

def get_ollama_controller() -> OllamaController:
    """
    Retorna a instancia del controlador de ollama.
    
    Returns:
        OllamaController: Controlador de ollama.
    """
    # Retorna el controlador.
    return __ollama_controller