# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/app.py
# Autor: Pablo González García
# Descripción: 
# Flujo principal del programa.
# -----------------------------------------------------------------------------

# ---- MÓDULOS ---- #
import logging

from common.log.logger import get_logger

from ollama.server import OllamaServer
from ollama.client import OllamaClient
from ollama.schema import Response
from ollama.model import model_installed, install_model

from chat.session import ChatSession

from config.context import CONFIG

# ---- FLUJO PRINCIPAL ---- #
if __name__ == "__main__":
    
    # -- Variables -- #
    logger:logging.Logger = get_logger(name=__name__, file="app.log")       # Inicializa el logger.
    server:OllamaServer = OllamaServer()                                    # Inicializa el servicio Ollama.
    session:ChatSession = ChatSession()                                     # Inicializa la sesión.
    
    # -- Lógica principal -- #
    logger.info("Ejecución del programa iniciado.")
    server.Start()              # Comienza la ejecución del servicio Ollama.
    
    # Comprueba si el modelo esta instalado. En caso de que no 
    # lo este, lo instala.
    if not model_installed(CONFIG.model.name):
        logger.warning(f"No se ha encontrado el modelo {CONFIG.model.name}.")   # Imprime información.
        # Instala el modelo.
        install_model(CONFIG.ollama.executablePath, CONFIG.model.name)
        logger.info(f"Modelo ({CONFIG.model.name}) instalado correctamente.")   # Imprime información.
    # En caso de que exista el modelo.
    else:
        logger.info(f"Modelo ({CONFIG.model.name}) disponible.")   # Imprime información.
        
    try:
        session.Start()                                             # Inicia el chat.

    except KeyboardInterrupt:
        logger.info(f"Ctrl+C Detectado. Finalizada ejecución del programa.")
        server.Stop()           # Finaliza la ejecución del servicio Ollama.
    except Exception as e:
        logger.error(f"Error: {e}")
        server.Stop()           # Finaliza la ejecución del servicio Ollama.
    
    server.Stop()               # Finaliza la ejecución del servicio Ollama.