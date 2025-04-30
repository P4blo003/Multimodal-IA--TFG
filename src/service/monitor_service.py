# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/service/monitor_service.py
# Autor: Pablo González García
# Descripción: Servicio de ingesta contniua de documentos basado
# en observador.
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
from ingestion.document_loader import DocumentLoader
from ingestion.observer import start_directory_watcher
from utils.logger import get_logger

# ---- Parámetros ---- #
logger = get_logger(__name__)

# ---- Funciones ---- #
def continuous_ingestion(cfg:dict):
    """
    Inicia un servicio de ingesta continua que observa un directorio y carga
    nuevos documentos en caliente mediante DocumentLoader.
    
    param dict cfg:
        Diccionario de configuración global del sistema.
    """
    backend:str = cfg.get('documents', {}).get('backend', 'haystack')
    loader:DocumentLoader = DocumentLoader(cfg=cfg, backend=backend)
    
    # Crea la función a realizar cuando haya un nuevo archivo.
    def on_new_file(file_path:str):
        """
        Callback invocada cuando se detecta un nuevo archivo en el directorio.
        Reutiliza la instancia de DocumentLoader para procesar el nuevo documento.
        
        param str file_path:
            Ruta del archivo recientemente detectado.
        """
        logger.info(f"Nuevo documento detectado: {file_path}. Procesando ...")
        try:
            loader.load_and_index()
        except Exception as ex:
            logger.error(f"Error durante la ingesta de {file_path}: {ex}")
    
    path:str = cfg.get('documents', {}).get('path', None)
    valid_extensions:list[str] = cfg.get('documents', {}).get('valid_extensions', [".pdf", ".docx", ".txt", ".csv", ".xlsx"])
    
    logger.info("Iniciando observador de directorio para ingesta continua ...")
    observer = start_directory_watcher(path_to_watch=path, callback=on_new_file, valid_extensions=valid_extensions)
    logger.info("Observador activo. El sistema esta listo para recibir nuevos documentos.")
    return observer