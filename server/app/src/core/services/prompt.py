# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: prompt.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones relacionadas con la construcción de prompts.   
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
from typing import List, Dict
# Librerías externas
from jinja2 import Environment, FileSystemLoader, Template
# Librerías internas
from model.context import ContextDTO
from config.schema.prompt import PromptConfig


# ---- CLASES ---- #
class PromptService:
    """
    Proporciona métodos relacionados con los prompts.
    """
    # -- Método por defecto -- #
    def __init__(self, prompt_cfg:PromptConfig):
        """
        Inicializa la instancia.
        
        Args:
            prompt_cfg (PromptConfig): Configuración del prompt.
        """
        # Inicializa los parámetros.
        self.__template:Template = Environment(loader=FileSystemLoader(prompt_cfg.root)).get_template(prompt_cfg.chatPrompt)
    
    # -- Métodos públicos -- #
    def build_prompt(self, query:str, context:List[ContextDTO], history:List[Dict[str,str]]) -> str:
        """
        Construye el prompt a partir de los datos dados.
        
        Args:
            context (List[ContextDTO]): Listado con el contexto.
            history (List[Dict[str,str]]): Historial del chat.
            query (str): Consulta del usuario.
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            str: Prompt construido.
        """
        # Try-Except para manejo de errores.
        try:
            # Retorna el prompt.
            return self.__template.render(
                context=context,
                history=history,
                query=query
            )
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"PromptService.build_prompt() -> [{type(e).__name__}] No se ha podido construir el prompt. Trace: {e}")