# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/utils/log/schema.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases relacionadas con ollama.
# -----------------------------------------------------------------------------


# ---- Módulos ---- #
from dataclasses import dataclass


# ---- Clases de datos ---- #
@dataclass
class Response:
    """
    Almacena la respuesta del modelo de Ollama.
    
    Attributes:
        mdel (str): Nombre del modelo.
        response (str): Respuesta del modelo.
        tokens_prompt (int): Número de tokens del prompt.
        generated_tokens (int): Número de tokens generados.
        total_time (float): Tiempo total de la petición.
        load_model_time (float): Tiempo de carga del modelo.
        eval_prompt_time (float): Tiempo de evaluación del prompt.
        generation_time (float): Tiempo de generación de la respuesta.
    """
    # -- Parámetros -- #
    model:str = None
    response:str = None
    tokens_prompt:int = None
    generated_tokens:int = None
    total_time:float = None
    load_model_time:float = None
    eval_prompt_time:float = None
    generation_time:float = None