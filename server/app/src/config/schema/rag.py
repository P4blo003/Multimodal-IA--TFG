# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: rag.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene las clases con las configuraciones de RAG.  
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
from .common import EmbeddingModelConfig


# ---- CLASES ---- #
class DocumentConfig(BaseModel):
    """
    Almacena la configuración del RAG  de documentos.
    
    Attributes:
        framework (str): Framework empleado.
        docDir (str): Directorio raiz con los documentos.
        storeDir (str): Directorio raiz con los almacenes de documentos.
        splitLength (int): Tamaño del chunk en tokens.
        splitOverlap (int): Overlap para mantener xontexto entre chunks.
        topK (int): El número de chunks más relevantes.
    """
    # -- Atributos -- #
    framework:str       = Field(default='HAYSTACK')
    docDir:str          = Field(default='data/raw')
    storeDir:str        = Field(default='rag/storage')
    splitLength:int     = Field(default=500, ge=1)
    splitOverlap:int    = Field(default=50, ge=1)
    topK:int            = Field(default=10, ge=1)


class RagConfig(BaseModel):
    """
    Almacena la configuración de RAG.
    
    Attributes:
        installModelDir (str): Directorio raiz de instalación de modelos.
        model (EmbeddingModelConfig): Configuración del modelo de embeddings.
        document (DocumentConfig): Configuración del RAG de documentos.
    """
    # -- Atributos -- #
    installModelDir:str
    model:EmbeddingModelConfig
    document:DocumentConfig