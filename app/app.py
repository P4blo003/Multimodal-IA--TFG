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
from common.logger import get_logger

from ollama.server import OllamaServer


# ---- FLUJO PRINCIPAL ---- #
if __name__ == "__main__":
    
    # -- Variables -- #
    logger:logging.Logger = get_logger(name=__name__, file="app.log")       # Inicializa el logger.
    ollama_server:OllamaServer = OllamaServer()                                    # Inicializa el servicio Ollama.
    
    # -- Lógica principal -- #
    logger.info("Ejecución del programa iniciado.")
    ollama_server.Start()              # Comienza la ejecución del servicio Ollama.
    
    ollama_server.Stop()               # Finaliza la ejecución del servicio Ollama.
    logger.info("Ejecución del programa detenida.")