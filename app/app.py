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
from utils.log.logger import get_logger

from config.context import LOG_CFG

# ---- Main ---- #
if __name__ == "__main__":
    
    # ---- Declaración de variables globales ---- #
    logger:logging.Logger = get_logger(name=__name__, file="app.log", cfg=LOG_CFG)      # Crea el logger de main.
    
    # ---- Declaración de funciones ---- #
    def end_program(exit_value:int = 0):
        """
        Finaliza el programa. Muestra un mensaje en el log informando del código de salida
        del mismo.
        
        Args:
            exit_value (int): Valor de salida del programa. Por defecto vale 0.
        """
        logger.info(f"Finalizado programa ({exit_value})")  # Imprime el mensaje.
        exit(exit_value)        # Finaliza el programa con el código de salida.
        
    # ---- Lógica principal ---- #
    logger.info("Iniciado programa.")   # Imprime el inicio del programa.
        
    
    end_program(exit_value=0)           # Finaliza el programa.