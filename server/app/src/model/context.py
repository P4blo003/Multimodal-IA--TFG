# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: context.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene las clases con la información del contexto.
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
class ContextDTO(BaseModel):
    """
    Almacena los datos del contexto.
    
    Attributes:
        score (float): Puntuación obtenida por el modelo.
        sourceType (str): Tipo de objeto de donde se obtuvo (DOCUMENT/SQL)
        surceDir (str): Ruta del fichero.
        content (str): Contenido del contexto. 
    """
    # -- Atributos -- #
    score:float
    sourceType:str
    sourceDir:str
    content:str