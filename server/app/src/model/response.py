# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: response.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene las clases con la información de las respuestas.
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar

# Librerías externas
from pydantic import BaseModel
# Librerías internas


# ---- CLASES ---- #
class BaseResponseDTO(BaseModel):
    """
    Almacena la los datos de la respuesta.
    
    Attributes:
        content (str): Contenido de la respuesta del modelo.
    """
    # -- Atributos -- #
    content:str