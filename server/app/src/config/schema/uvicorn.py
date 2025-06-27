# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: uvicorn.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene las clases con las configuraciones de Uvicorn.    
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
from .common import HostConfig


# ---- CLASES ---- #
class UvicornConfig(BaseModel):
    """
    Almacena la configuración de Uvicorn.
    
    Attributes:
        host (HostConfig): Configuración del host.
        reload (bool): Si recarga el servicio al modificar los scripts.
    """
    # -- Atributos -- #
    host:HostConfig
    reload:bool = False
    