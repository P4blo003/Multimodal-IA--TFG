
# ---- MÓDULOS ---- #
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2 import Template

from typing import List, Dict

from .base import PromptStrategy

# ---- CLASES ---- #
class JinjaPrompt(PromptStrategy):
    """
    Estrategia de prompting basada en plantillas Jinja2.
    Usa historial estructurado.
    """
    # -- Métodos por defecto -- #
    def __init__(self, template_name:str="prompt.j2",
                 template_dir:Path=Path("config"),
                 system_prompt:str="Eres un asistente inteligente para una planta industrial."):
        """
        Inicializa el motor de plantillas Jinja2 y carga la plantilla seleccionada.
        
        Args:
            template_name (str): Nombre del archivo de plantilla Jinja2.
            template_dir (Path): Ruta al directorio que contiene la plantilla.
            system_prompt (str): Intrucción base que el asistente debe seguir.
        """
        self.__systemPrompt:str = system_prompt
        self.__env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape()
        )
        self.__template:Template = self.__env.get_template(template_name)

    
    # -- Métodos públicos -- #
    def build_prompt(self, user_input:str, history:List[Dict[str, str]]):
        """
        Construye el prompt usando el historial y el input del usuario.
        
        Args:
            user_input (str): Input del usuario.
            history (List[Dict[str, str]]): Historial del chat.
        """
        return self.__template.render(
            system_prompt=self.__systemPrompt,
            user_input=user_input,
            history=history
        )