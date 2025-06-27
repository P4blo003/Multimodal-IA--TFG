# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: measure.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene las clases con la información de las mediciones.
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar

# Librerías externas
from pydantic import BaseModel
from pydantic import Field
# Librerías internas



# ---- CLASES ---- #
class OllamaModelDataDTO(BaseModel):
    """
    Almacena los parámetros obtenidos por la API de Ollama del modelo.
    
    Attributes:
        totalDuration (float): Tiempo empleado en generar la respuesta.
        loadDuration (float): Tiempo empleado en cargar el modelo.
        promptEvalCount (float): Número de tokens en el prompt.
        promptEvalDuration (float): Tiempo empleado en evaluar el prompt.
        evalCount (float): Número de tokens en la respuesta generada.
        evalDuration (float): Tiempo empleado en generar la respuesta.
        speed (float): Velocidad del modelo. Reprsenta el número de toknes generados, grente
            al tiempo empleado.
    """
    # -- Atributos -- #
    totalDuration:float
    loadDuration:float
    promptEvalCount:float
    promptEvalDuration:float
    evalCount:float
    evalDuration:float
    speed:float


class RagModelDataDTO(BaseModel):
    """
    Almacena los parámetros obtenidos del modelo de embedding del rag.
    
    Attributes:
        action (str): Acción que ha realizado.
            - EMBEDDING.
            - RETRIEVE.
        duration (float): Duración en realizar la acción.
    """
    # -- Atributos -- #
    action:str = Field(pattern='EMBEDDING|RETRIEVE')
    duration:float