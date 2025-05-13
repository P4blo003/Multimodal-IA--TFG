# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/ollama/model.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene funciones relacionadas con los modelos de Ollama,
# como el listado o instalación.
# -----------------------------------------------------------------------------

# ---- Múdulos ---- #
import os
import subprocess

import requests

from config.context import ENV

# ---- Funciones ---- #
def model_installed(model_name:str) -> bool:
    """
    Comprueba si el modelo de ollama existe.
    
    Args:
        model_name (str): Nombre del model.
    Returns:
        bool: True si el modelo existe y False en otro caso.
    """
    # Crea la URL completa.
    url:str = f"http://{ENV['OLLAMA_HOST']}/api/tags"
    # Solicita la lista de modelos al servicio ollama.
    response = requests.get(url)
    response.raise_for_status()  # Lanza un error si la respuesta no es 200
    # Obtiene la respuesta en formato JSON.
    models = response.json().get("models", [])
    # Comrpueba si existe algún modelo con el nombre dado.
    exist = any(model.get("name", "").startswith(model_name) for model in models)
    # Devuelve si existe o no.
    return exist
    
def install_model(bin_path:str, model:str):
    """
    Instala el modelo de Ollama.
    
    Args:
        bin_path (str): Ruta al binario de Ollama.
        model (str): Nombre del modelo a instalar.
    """
    with open(os.devnull, 'w') as devnull:
        process = subprocess.run(
            [bin_path, "pull", model],
            check=True,
            stdout=devnull,
            stderr=devnull
        )