# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/external/ollama/model.py
# Autor: Pablo González García
# Descripción: 
# Módulo encargado de las funciones relacionadas con los modelos
# de Ollama.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import requests
from subprocess import Popen

from common.process import start_subprocess


# ---- FUNCIONES ---- #
def model_installed(ollama_url:str, model_name:str) -> bool:
    """
    Devuelve si el modelo de Ollama está instalado o no.
    
    Args:
        ollama_url (str): Url del servicio de Ollama.
        model_name (str): Nombre del modelo.
    
    Returns:
        bool: True si el modelo está instalado y False en caso contrario.
    """
    # Genera la url de la API.
    __apiUrl:str = f"{ollama_url}/api/tags"
    
    # Solicita la lista de modelos al servicio ollama.
    response = requests.get(__apiUrl)
    response.raise_for_status()  # Lanza un error si la respuesta no es 200
    
    # Obtiene la respuesta en formato JSON.
    __models = response.json().get("models", [])
    
    # Comrpueba si existe algún modelo con el nombre dado.
    __exist = any(model.get("name", "").startswith(model_name) for model in __models)
    
    # Devuelve si existe o no.
    return __exist

def install_model(bin_path:str, model_name:str, env:dict=None) -> any:
    """
    Instala el modelo mediante el servicio de Ollama.
    
    Args:
        bin_path (str): Ruta el directorio del binario de Ollama.
        model_name (str): Nombre del modelo de Ollama.
        env (dict): Variables de entorno para el subproceso.
    """
    # Inicia un subproceso que instale el modelo.
    __args = [bin_path]+["pull"] + [model_name]
    __process:Popen = start_subprocess(args=__args, env=env)
    __process.wait()                    # Espera a que finalice el proceso.