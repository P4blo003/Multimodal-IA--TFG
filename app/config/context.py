# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/config/context.py
# Autor: Pablo González García
# Descripción:
# 
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import os
from dotenv import load_dotenv
import yaml

from utils.log.classes import LoggerConfig
from ollama.classes import OllamaConfig

# ---- Parámetros ---- #
LOG_CFG:LoggerConfig = LoggerConfig()       # Configuración del logger.
OLLAMA_CFG:OllamaConfig = OllamaConfig()    # Configuración de ollama.

# ---- Inicialización ---- #
load_dotenv()       # Carga las variables de entorno.
__settings_file:str = os.getenv('SETTINGS_FILE')        # Obtiene la ruta del fichero de configuración.

if os.path.exists(__settings_file):                     # Si existe el fichero.
    # Abre el fichero.
    with open(__settings_file, 'r', encoding='utf-8') as file:
        cfg = yaml.safe_load(file)                      # Obtiene los datos del archivo.
        
        if cfg:         # Si obtiene algún dato.
            logger_cfg = cfg.get('logger', {})          # Obtiene los parámetros para logger.
            
            if logger_cfg:          # Si obtiene algún campo.
                LOG_CFG.level = logger_cfg.get('level', LOG_CFG.level)
                LOG_CFG.format = logger_cfg.get('format', LOG_CFG.format)
                LOG_CFG.datefmt = logger_cfg.get('datefmt', LOG_CFG.datefmt)
                LOG_CFG.path = logger_cfg.get('path', LOG_CFG.path)
                LOG_CFG.maxBytes = logger_cfg.get('max_bytes', LOG_CFG.maxBytes)
                LOG_CFG.backupCount = logger_cfg.get('backup_count', LOG_CFG.backupCount)
            

            ollama_cfg = cfg.get('ollama', {})          # Obtiene los parámetros para ollama.
            
            if ollama_cfg:          # Si obtiene algún campo.
                OLLAMA_CFG.host = ollama_cfg.get('host', OLLAMA_CFG.host)
                OLLAMA_CFG.port = ollama_cfg.get('port', OLLAMA_CFG.port)
                OLLAMA_CFG.bin = ollama_cfg.get('bin', OLLAMA_CFG.bin)
                OLLAMA_CFG.silent = ollama_cfg.get('silent', OLLAMA_CFG.silent)
                OLLAMA_CFG.file = ollama_cfg.get('file', OLLAMA_CFG.file)