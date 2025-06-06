# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/main.py
# Autor: Pablo González García
# Descripción: 
# Punto de entrada del servidor. Configura el servidor, inicia los
# servicios auxiliares como OllamController y gestiona el ciclo de vida
# del servidor.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import uvicorn
from core.dependencies import get_ollama_controller

from logging import Logger
from utilities.logger import create_logger

from config.context import CFG, ENV


# ---- VARIABLES GLOBALES ---- #
logger:Logger = create_logger(logger_name='uvicorn', cfg=CFG.logger, console=True, file='server.log')


# ---- FUNCIONES GLOBALES ---- #
def start_services() -> None:
    """
    Inicializa los servicios del servidor.
    """
    # Inicializa los servicios de Ollama.
    get_ollama_controller().start_api(ollama_cfg=CFG.ollama, system_cfg=CFG.system, env=ENV)
    get_ollama_controller().check_model(ollama_cfg=CFG.ollama, env=ENV)

def stop_services() -> None:
    """
    Finaliza los servicioes del servidor.
    """
    # Finaliza los servicios de Ollama.
    get_ollama_controller().stop_api()


# ---- FLUJO PRINCIPAL ---- #
if __name__ == "__main__":
    
    # -- Inicialización -- #    
    # Try-except para manejo de excepciones:
    try:
        # Inicial los servicios del servidor.
        start_services()
        # Inicia uvicorn para poder acceder desde otros equipos.
        uvicorn.run("api.main:app", host=CFG.uvicorn.host, port=CFG.uvicorn.port, reload=CFG.uvicorn.reload, log_config=None)
    
    # Si se detecta un Ctrl+C
    except KeyboardInterrupt:
        # Imprime información.
        print()                 # Imprime un salto de línea.
        logger.warning("Ctrl+C detectado. Finalizando el servidor ...")
    
    # Si ocurre alguna excepción.
    except Exception as e:
        logger.error(e)  # Imprime el error.

    # Funciones a ejecutar al final.
    finally:
        # Finaliza los servicios del servidor.
        stop_services()