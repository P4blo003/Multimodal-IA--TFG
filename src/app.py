# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/app.py
# Autor: Pablo González García
# Descripción: Flujo principal del programa.
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import logging

from ingestion.document_loader import DocumentLoader

from utils.logger import get_logger

# ---- Funciones ---- #
def end_prog(logger:logging.Logger, exit_value:int = 0):
    """
    Imprime el mensaje de finalización del programa con el valor de salida.
    
    Args:
        logger (logging.Logger): Logger para mostrar el mensaje.
        exit_value (int): Valor de salida.
    """
    logger.info(f"Finalizado programa MULTIMODAL-IA ({exit_value})")        # Imprime el mensaje.
    exit(exit_value)                                                        # Finaliza el programa con el valor de salida.

# ---- Main ---- #
if __name__ == "__main__":
    # Inicializa el logger.
    logger: logging.Logger = get_logger(__name__)               # Crea el logger para el script __main__.
    
    # -- Lógica principal -- #
    logger.info("Iniciado programa MULTIMODAL-IA")
    
    # Inicializa las variables del sistema.
    documentLoader:DocumentLoader = DocumentLoader()           # Inicializa el document loader.
    
    end_prog(logger=logger, exit_value=0)       # Finaliza el programa.