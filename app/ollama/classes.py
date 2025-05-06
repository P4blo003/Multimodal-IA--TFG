# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/utils/log/classes.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases relacionadas con ollama.
# -----------------------------------------------------------------------------

# ---- Módulos ---- #
from dataclasses import dataclass

# ---- Clases ---- #
@dataclass
class OllamaConfig:
    """
    Clase que almacena la configuración de ollama.
    
    Attributes:
        host (str): Host del servicio de ollama.
        port (int): Puerto del servicio de ollama.
        bin (str): Ruta al fichero binario de ollama.
        silent (bool): Si se debe mostrar los mensajes de ollama.
        file (str): Ruta al fichero de logs.
    """
    # -- Parámetros -- #
    host:str = '0.0.0.0'
    port:int = 11434
    bin:str = 'bin/ollama/ollama'
    silent:bool = False
    file:str = 'logs/ollama_serve.log'