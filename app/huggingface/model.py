# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/huggingface/model.py
# Autor: Pablo González García
# Descripción: 
# Módulo para la gestión y descarga de modelos desde Hugging Face.
# Proporciona finciones para obtener el nombre real del modelo y para instalar
# modelos en un directorio local, con opción de salida silenciosa.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
import io
from contextlib import redirect_stderr, redirect_stdout

from huggingface_hub import snapshot_download


# ---- FUNCIONES ---- #
def get_real_name(hugging_name:str) -> str:
    """
    Obtiene el nombre real del modelo. Esta función ayuda a procesar los nombres de los
    modelos de hugging face, ya que vienen de la forma `sentence-transformer/nombre`
    
    Args:
        hugging_name (str): El nombre del modelo obtenido de hugging face.
    
    Returns:
        str: El nombre real del modelo.
    """
    # Separa el nombre por el caracter '/'.
    values:list = hugging_name.split("/")
    return values[len(values)-1]    # Retorna el último elemento.

def install_model(model_name:str, dir:str, silent:bool=False) -> str:
    """
    Instala el modelo de hugging face en un directorio local.
    
    Args:
        model_name (str): Nombre completo del modelo a instalar.
        dir (str): Directorio donde se almacenan los modelos.
        silent (bool): Si la salida debe ser silenciosa.
        
    Returns:
        str: La ruta donde se almacenó el modelo o None.
    """
    # Si la salida debe ser silenciosa.
    if silent:
        fnull = io.StringIO()
        with redirect_stdout(fnull), redirect_stderr(fnull):
            # Instala el modelo.
            path = snapshot_download(repo_id=model_name, cache_dir=dir)
    # Si la salida no debe ser silenciosa.
    else:
        # Instala el modelo.
            path = snapshot_download(repo_id=model_name, cache_dir=dir)
    # Comprueba si el directorio existe.
    if os.path.exists(path=path):
        return path     # Retorna el directorio.
    return None         # Retorna None.