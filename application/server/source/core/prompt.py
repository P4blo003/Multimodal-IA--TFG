# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/core/prompt.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene la clase con las funcionalidades para
# crear los prompts en función de un template.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
from typing import List, Dict, Tuple
from jinja2 import Environment, FileSystemLoader, Template
from config.schema import PromptConfig


# ---- CLASES ---- #
class PromptBuilder:
    """
    Clase que se encarga de gestionar la construcción del prompt.
    """
    # -- Métodos por defecto -- #
    def __init__(self, prompt_cfg:PromptConfig):
        """
        Inicializa la instancia.
        
        Args:
            prompt_cfg (PromptConfig): Configuración del prompt.
        """
        # Inicializa las propiedades.
        self.__env:Environment = None
        self.__template:Template = None
        
        self.__create_jinja_env(prompt_cfg=prompt_cfg)
    
    
    # -- Métodos privados -- #
    def __create_jinja_env(self, prompt_cfg:PromptConfig) -> None:
        """
        Crea las dependencias necesarias para jinja2.
        
        Args:
            prompt_cfg (PromptConfig): Configuración del prompt.
        """
        # Extrae el directorio y el nombre del archivo de la plantilla.
        template_dir, template_file = os.path.split(prompt_cfg.templateFile) 
        # Carga el entorno de Jinja2
        self.__env = Environment(loader=FileSystemLoader(template_dir))
        self.__template = self.__env.get_template(template_file)
    
    # -- Métodos públicos -- #
    def create_prompt(self, context:List[Tuple[str, float]], chat_history:List[Dict[str, str]], query:str) -> str:
        """
        Crea un prompt usando una plantilla Jinja2 desde archivo.

        Args:
            context (List[Tuple[str, float]]): Lista de tuplas con (contenido, score).
            chat_history (List[Dict[str, str]]): Historial de mensajes del chat, cada uno con 'role' y 'content'.
            query (str): Consulta actual del usuario.

        Returns:
            str: Prompt generado a partir de la plantilla.
        """
        # Prepara el contexto para la plantilla
        context_texts = [chunk for chunk, _ in sorted(context, key=lambda x: -x[1])]  # ordenado por score
        
        # Renderiza la plantilla
        prompt = self.__template.render(
            context=context_texts,
            history=chat_history,
            user_input=query
        )
        
        # Retorna el prompt.
        return prompt