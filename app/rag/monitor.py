# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/rag/monitor.py
# Autor: Pablo González García
# Descripción: Servicio de ingesta continua de documentos basado
# en observador.
# -----------------------------------------------------------------------------

# ---- MÓDULOS ---- #
from .observer import start_directory_watcher

import logging
from common.log.logger import get_logger

from config.context import CONFIG

# ---- PARÁMETROS ---- #
logger:logging.Logger = get_logger(name=__name__, file="app.log", console=False)

# ---- FUNCIONES ---- #
def init_continuous_ingestion():
    """
    Inicia un servicio de ingesta continua que observa un directorio y carga
    nuevos documentos en caliente mediante DocumentLoader.
    """
    # Crea la función a realizar cuando haya un nuevo archivo.
    def on_new_file(file_path:str):
        """
        Callback invocada cuando se detecta un nuevo archivo en el directorio.
        Reutiliza la instancia de DocumentLoader para procesar el nuevo documento.
        
        Args:
            file_path (str): Ruta del archivo recientemente detectado.
        """
        logger.info(f"Nuevo documento detectado: {file_path}. Procesando ...")
    
    logger.info(f"Iniciando observer de documentos PATH: {CONFIG.rag.docDirectory}")
    observer = start_directory_watcher(path_to_watch=CONFIG.rag.docDirectory, callback=on_new_file)
    logger.info(f"Observador activo.")
    
    return observer