# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: common.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases de configuraciones comunes.   
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
class HostConfig(BaseModel):
    """
    Almacena la configuración de un host.
    
    Attributes:
        ip (str): IP del host.
        port (int): Puerto del host.
    """
    # -- Atributos -- #
    ip:str = Field(default='localhost')
    port:int = Field(default=49152, ge=49152, le=65535)


class BaseModelConfig(BaseModel):
    """
    Almacena la configuración de un modelo.
    
    Attributes:
        tag (str): Etiqueta del modelo.
    """
    # -- Atributos -- #
    tag:str
    

class EmbeddingModelConfig(BaseModelConfig):
    """
    Almacena la configuración de un modelo de embeddings.
    
    Attributes:
        tag (str): Etiqueta del modelo.
        embeddingDim (int): Tamaño de los embeddings.
    """
    # -- Atributos -- #
    embeddingDim:int