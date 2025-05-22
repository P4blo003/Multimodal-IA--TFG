# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/ollama/model.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene funciones relacionadas con los modelos de Ollama,
# como el listado o instalación.
# -----------------------------------------------------------------------------


# ---- Múdulos ---- #
import os
import subprocess
import requests


# ---- Funciones ---- #
def model_installed(ollama_host:str, model_name:str) -> bool:
    """
    Comprueba si el modelo de ollama existe.
    
    Args:
        ollama_host (str): Host de ollama en la forma IP:Puerto.
        model_name (str): Nombre del model.
    Returns:
        bool: True si el modelo existe y False en otro caso.
    """
    # Crea la URL completa.
    url:str = f"http://{ollama_host}/api/tags"
    # Solicita la lista de modelos al servicio ollama.
    response = requests.get(url)
    response.raise_for_status()  # Lanza un error si la respuesta no es 200
    # Obtiene la respuesta en formato JSON.
    models = response.json().get("models", [])
    # Comrpueba si existe algún modelo con el nombre dado.
    exist = any(model.get("name", "").startswith(model_name) for model in models)
    # Devuelve si existe o no.
    return exist
    
def install_model(bin_path:str, model_name:str):
    """
    Instala el modelo de Ollama.
    
    Args:
        bin_path (str): Ruta al binario de Ollama.
        model_name (str): Nombre del modelo a instalar.
    """
    with open(os.devnull, 'w') as devnull:
        process = subprocess.run(
            [bin_path, "pull", model_name],
            check=True,
            stdout=devnull,
            stderr=devnull
        )