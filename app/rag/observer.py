# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/rag/observer.py
# Autor: Pablo González García
# Descripción: 
# Observador de directorio para ingesta continua de documentos.
# -----------------------------------------------------------------------------

# ---- MÓDULOS ---- #
import os
from pathlib import Path
from typing import List

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import logging
from common.log.logger import get_logger

from config.context import CONFIG

# ---- CLASES ---- #
class NewFileHandler(FileSystemEventHandler):
    """
    Manejador de eventos que detecta nuevos archivos en un directorio y ejecuta
    una función callback si el archivo tiene una extensión válida.
    """
    # -- Métodos por defecto -- #
    def __init__(self, callback):
        """
        Inicializa el manejador de eventos.
        
        Args:
            callback: Función a ejecutar cuando se detecta un nuevo archivo
            válido.
        """
        self.__callback = callback
    
    # -- Métodos públicos -- #
    def on_created(self, event):
        """
        Método invocado automáticamente por watchdog cuando se crea un archivo.
        Verifica si es válido y ejecuta la función callback.
        """
        # Si es un directorio.
        if event.is_directory:
            return
        
        path:Path = Path(event.src_path) 
        ext = path.suffix
        if ext.lower() in CONFIG.rag.validExtensions:
            self.__callback(event.src_path)
    

# ---- FUNCIONES ---- #
def start_directory_watcher(path_to_watch:str, callback):
    """
    Inicia un observador de cambios en el sistema de archivos.
    
    Args:
        path_to_watch (str): Ruta al directorio a observar.
        callback: Función a llamar cuando se detecta un nuevo archivo válido.
    Returns:
        Observer activo.
    """
    observer = Observer()
    handler = NewFileHandler(callback=callback)
    observer.schedule(handler, path=path_to_watch, recursive=False)
    observer.start()
    # Retorna el observador.
    return observer