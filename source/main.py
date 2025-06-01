# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/main.py
# Autor: Pablo González García
# Descripción: 
# Flujo principal del programa.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from logging import Logger
from common.logger import create_logger

from external.ollama.core import OllamaManager
from chat.session import ChatSession


# ---- LÓGICA PRINCIPAL ---- #
if __name__ == "__main__":
    
    # -- Variables locales -- #
    logger:Logger = create_logger(logger_name=__name__, file='app.log')
    ollamaManager:OllamaManager = OllamaManager()
    chatSession:ChatSession = None
    
    # -- Flujo principal -- #
    logger.info("Inicio de ejecición del programa.")        # Imprime información.
    
    # Try-except para manejar posibles excepciones.
    try:
        ollamaManager.StartService()        # Comienza el servicio de Ollama.
        ollamaManager.CheckModel()          # Comprueba que el modelo de Ollama esté instalado.
        
        chatSession = ChatSession(ollama_url=ollamaManager.Url)         # Inicializa la sesión de chat.
        chatSession.StartChat()             # Comienza el chat.
    
    except Exception as e:
        logger.error(f"Ha ocurrido un error durante la ejecución. ERROR: {e}")      # Imprime información
    
    ollamaManager.StopService()             # Finaliza el serviciio de Ollama.
    logger.info("Fin de la ejecición del programa.")                                # Imprime información.