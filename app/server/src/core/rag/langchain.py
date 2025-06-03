# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/backend/langchain/prompt.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene funciones relacionadas con el prompting de langchain.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os

from jinja2 import Template


# ---- FUNCIONES ---- #
def create_prompt_template(file_path:str) -> Template:
    """
    Crea y configura un prompt template.
    
    Args:
        file_path (str): Ruta al fichero del template.
    
    Raises:
        FileNotFoundError: Si no se encuentra el fichero del template.
        
    Returns:
        Template: Prompt template configurado.
    """
    # Comprueba si el fichero existe.
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El fichero no existe. PATH: {file_path}")

    # Si el fichero si existe.
    with open("config/prompt.template.txt", "r", encoding="utf-8") as file:
        template = file.read()
        
    # Devuelve el prompt template.
    return Template(template)