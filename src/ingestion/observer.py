# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/ingestion/observer.py
# Autor: Pablo González García
# Descripción: Observador de directorio para ingesta continua de documentos.
# -----------------------------------------------------------------------------

# ---- Módulos ---- #
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils.logger import get_logger

# ---- Clases ---- #
class NewFileHandler(FileSystemEventHandler):
    """
    Manejador de eventos que detecta nuevos archivos en un directorio y ejecuta
    una función callback si el archivo tiene una extensión válida.
    """
    # -- Métodos por defecto -- #
    def __init__(self, callback, file_extensions: list[str]):
        """
        Inicializa el manejador de eventos.
        
        param callback:
            Función a ejecutar cuando se detecta un nuevo archivo
            válido.
        param list[str] file_extensions:
            Lista de extensiones válidas.
        """
        # Inicializa las propiedades.
        self.__callback = callback
        self.__validExtension:list[str] = file_extensions
        self.__logger = get_logger(__name__)
    
    # -- Métodos -- #
    def on_created(self, event):
        """
        Método invocado automáticamente por watchdog cuando se crea un archivo.
        Verifica si es válido y ejecuta la función callback.
        """
        if event.is_directory:
            return
        _, ext = os.path.splitext(event.src_path)
        if ext.lower() in self.__validExtension:
            self.__callback(event.src_path)

# ---- Funciones ---- #
def start_directory_watcher(path_to_watch:str, callback, valid_extensions:list[str]):
    """
    Inicia un observador de cambios en el sistema de archivos.
    
    param str path_to_watch:
        Ruta del directorio a observar.
    param callback:
        Función a llamar cuando se detecta un nuevo archivo
        válido.
    param list[str] valid_extensions:
        Lista de extensiones válidas a observar.

    Returns:
        Observer activo.
    """
    observer = Observer()
    handler = NewFileHandler(callback=callback, file_extensions=valid_extensions)
    observer.schedule(handler, path=path_to_watch, recursive=False)
    observer.start()
    return observer