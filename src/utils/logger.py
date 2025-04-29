# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/utils/logger.py
# Autor: Pablo González García
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import logging
import logging.handlers
import yaml
import os

# ---- Functions ---- #
def get_logger(name:str) -> logging.Logger:
    """
    Crea y configura un logger con nombre especificado.
    Lee la configuración de logging en config/settings.yaml si está disponible,
    sino usa parámetros por defecto.
    
    :param str name:
        El nombre del logger a crear.
    """
    logger:logging.Logger = None    # Variable a devolver.
    
    # Asigna los parámetros por defecto.
    log_level:str = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_format:str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_datefmt:str = '%Y-%m-%d %H:%M:%S'
    log_file = None
    max_bytes:int = 10 * 1024 * 1024    # 10 MB.
    backip_count:int = 5
    
    # Intenta cargar configuración desde YAML.
    try:
        with open('config/settings.yaml', 'r') as file:
            cfg = yaml.safe_load(file)      # Load de YAML file.
            logging_cfg = cfg.get('logging', {})
            
            log_level = logging_cfg.get('level', log_level).upper()
            log_format = logging_cfg.get('format', log_format)
            log_datefmt = logging_cfg.get('datefmt', log_datefmt)
            log_file = logging_cfg.get('file', log_file)
            max_bytes = logging_cfg.get('max_bytes', max_bytes)
            backip_count = logging_cfg.get('backup_count', backip_count)
        
    except Exception as ex:
        pass
    
    # Configurar el logger.
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # Evita añadir handlers duplicados.
    if not logger.handlers:
        # Crea un formateador común.
        formatter = logging.Formatter(fmt=log_format, datefmt=log_datefmt)
        
        # Crea el handler de consola.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level, logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Crea el handler de archivo rotativo si está configurado.
        if log_file:
            # Crea el archivo.
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backip_count, encoding='utf-8')
            file_handler.setLevel(getattr(logging, log_level, logging.INFO))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    return logger                   # Retorna el logger.