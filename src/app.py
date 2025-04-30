# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/app.py
# Autor: Pablo González García
# Descripción:
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import yaml
import time

from utils.logger import get_logger
from service.monitor_service import continuous_ingestion

# ---- Funciones ---- #
def end_program(value:int, logger):
    """
    Finaliza el programa, mostrando el valor de finalización.
    
    param int value:
        Valor de salida del programa.
    param logger:
        Logger para imprimir mensaje de información.
    """
    # Imprime la información y finaliza el programa.
    logger.info(f"Finalizado el programa. Exit Value: {value}")
    exit(value)

# ---- Main ---- #
if __name__ == "__main__":
    
    # -- Variables -- #
    logger = get_logger(__name__)          # Crea un logger para la aplicación.
    
    # Imprime información para saber cuando se cargo el programa.
    logger.info("Iniciada ejecución del programa.")
    
    # 1. Carga la configuración global.
    try:
        with open("config/settings.yaml") as file:
            cfg = yaml.safe_load(file)
        logger.info("Configuración cargada exitosamente.")
    except Exception as ex:
        logger.critical(f"Error al cargar configuración: {ex}")
        end_program(value=1, logger=logger)     # Finaliza el programa con código 1.
    
    # 2. Iniciar la ingesta continua de documentos.
    backend = cfg.get('documents', {}).get('backend', 'haystack')
    continuous_ingestion(cfg=cfg, backend=backend)
    
    end_program(value=0, logger=logger)     # Finaliza el programa con código 0.