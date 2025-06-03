# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/src/main.py
# Autor: Pablo González García
# Descripción: 
# Punto de entrada del servidor FastAPI. Configura el servidor, inicia los
# servicios uxiliares como OllamController y gestiona el ciclo de vida
# del servidor.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import sys
import signal
from types import FrameType

import uvicorn

from logging import Logger
from utils.logger import create_logger

from controller.ollama_controller import OllamaController

from config.context import CFG


# ---- VARIABLES GLOBALES ---- #
logger:Logger                       = create_logger(logger_name='uvicorn', cfg=CFG.logger, console=True, file='server.log')
ollama_controller:OllamaController  = OllamaController()


# ---- FUNCIONES GLOBALES ---- #
def start_services() -> None:
    """
    Inicializa los servicios externos necesarios para el funcionamiento del servidor.
    """
    ollama_controller.start_serve()     # Inicial el servicio de Ollama.

def stop_services() -> None:
    """
    Detiene los servicios externos de forma segura.
    """
    ollama_controller.stop_serve()      # Finaliza el servicio de Ollama.

def shutdown_handler(signum:int, frame:FrameType) -> None:
    """
    Manejador de señales para apagado controlado (SIGINT, SIGTERM).
    
    Args:
        signum (int): Número de señal recibida.
        frame (FrameType): Objeto que representa el marco de pila actual donde se recibió
            la señal.
    """
    print()         # Imprime un salto de línea.
    logger.warning(f"Señal de apagado recibida | SIG: {signum}")    # Imprime información de aviso.
    stop_services() # Detiene los servicios.
    sys.exit(0)     # Finaliza el programa.
    
    
# ---- REGISTRO DE SEÑALES ---- #
signal.signal(signalnum=signal.SIGTERM, handler=shutdown_handler)       # Para kill.


# ---- FLUJO PRINCIPAL ---- #
if __name__ == "__main__":
    
    # -- Inicialización -- #    
    # Try-except para manejo de excepciones:
    try:
        # Inicializa los servicios del servidor.
        start_services()
        # Inicia uvicorn para poder acceder desde otros equipos.
        uvicorn.run("app:api", host=CFG.uvicorn.host, port=CFG.uvicorn.port, reload=False, log_config=None, log_level="info")
    
    # En caso de que se detecte un Ctrl+C.
    except KeyboardInterrupt:
        logger.warning("Ctrl+C detectado")          # Imprime el aviso.
        stop_services()                             # Detiene los servicios.
    
    # En caso de que ocurra alguna excepción.
    except Exception as e:
        logger.error(f"Exception | E: {e}")         # Imprime el error.
    
    # Funciones a ejecutar al final.
    finally:
        stop_services()                             # Detiene los servicios.