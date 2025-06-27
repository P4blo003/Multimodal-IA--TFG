# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: query.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene las clases con la información de las peticiones.
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
class BaseQueryDTO(BaseModel):
    """
    Almacena la los datos de la query.
    
    Attributes:
        content (str): Contenido de la pregunta del cliente.
    """
    # -- Atributos -- #
    content:str