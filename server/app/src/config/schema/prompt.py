# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: prompt.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases de configuraciones de los prompts.   
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
class PromptConfig(BaseModel):
    """
    
    Attributes:
        root (str): Directorio raiz de los templates.
        chatPrompt (str): Nombre del fichero con el prompt del chat.
    """
    # -- Atributos -- #
    root:str        = Field(default='.server/etc/template')
    chatPrompt:str  = Field(default='chatPrompt.j2')