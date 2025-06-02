# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/server/src/utils/model.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene funciones relacionadas con los modelos de IA.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
import json

from huggingface_hub import snapshot_download

from contextlib import redirect_stdout, redirect_stderr


# ---- FUNCIONES ---- #
def model_installed(model_name:str, json_path:str) -> bool:
    """
    Comprueba si el modelo esta instalado en el sistema a partir
    de la información dada en el fichero json.
    
    Args:
        model_name (str): Nombre del modelo.
        json_path (str): Ruta al fichero json.
        
    Returns:
        bool: True si el modelo está instalado y False en caso contrario.
    """
    # Comprueba si el fichero no existe.
    if not os.path.exists(json_path):
        return False
    
    # Si el fichero existe.
    with open(json_path, 'r', encoding='utf-8') as file:
        data:dict = json.load(file)  # Carga los datos del fichero JSON.
    
    # Devuelve si el modelo esta en las claves o no.
    return model_name in data.keys()

def install_model(model_name:str, json_path:str, dir:str) -> str:
    """
    Instala el modelo desde hugging face, lo almacena en el directorio pasado por
    parámetro y almacena la información en el fichero json.
    
    Args:
        model_name (str): Nombre del modelo a instalar.
        json_path (str): Ruta del fichero json.
        dir (str): Ruta donde almacenar el modelo.
    
    Returns:
        str: Ruta donde se almacenó el modelo.
    """
    # Instala el modelo y obtiene el path donde lo descargar.
    with open(os.devnull, 'w') as devnull:
        with redirect_stdout(devnull), redirect_stderr(devnull):
            path:str = snapshot_download(repo_id=model_name, local_dir=os.path.join(dir, model_name))
    
    # Obtiene los modelos instalados del fichero.
    data:dict = {}
    # Comprueba si el directorio existe.
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # Carga los datos del fichero JSON.
    
    data[model_name] = path          # Establece el nuevo modelo instalado.
    
    # Almacena el nuevo modelo en un fichero.
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=1)
    
    # Devuelve el path donde se descargó.
    return path