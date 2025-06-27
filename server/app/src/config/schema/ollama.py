# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: ollama.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene las clases con las configuraciones de Ollama.  
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
from .common import HostConfig, BaseModelConfig


# ---- CLASES ---- #
class ServiceConfig(BaseModel):
    """
    Almacena la configuración de un servicio.
    
    Attributes:
        name (str): Nombre del servicio.
        host (HostConfig): Configuración del host.
        model (BaseModelConfig): Configuración del modelo.
    """
    # -- Atributos -- #
    name:str = Field(default='Default')
    host:HostConfig
    model:BaseModelConfig


class OllamaConfig(BaseModel):
    """
    Almacena la configuración de Ollama.
    
    Attributes:
        services (List[ServiceConfig]): Listado con la configuración de los distintos
            servicios disponibles.
    """
    # -- Atributos -- #
    service:ServiceConfig