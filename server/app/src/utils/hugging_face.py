# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: hugging_face.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones relacionadas con huggingFace.    
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
import os
from pathlib import Path
from typing import List
# Librerías externas
from huggingface_hub import snapshot_download
# Librerías internas
from utils.path import is_valid


# ---- FUNCIONES ---- #
def list_installed_models(root_path:Path) -> List[str]:
    """
    Lista los modelos instalados en el directorio.
    
    Args:
        root_path (Path): Path donde estan instalados los modelos.
    Raises:
        OSError: En caso de que haya algún error.
    Returns:
        List[str]: Listado con los modelos instalados.
    """
    # Try-Except para manejo de errores.
    try:
        # Comprueba si el path es válido.
        if is_valid(root_path=root_path):
            
            # Variable a retornar.
            models: List[str] = []
            
            # Recorremos primer nivel (por ejemplo 'sentence-transformers')
            for namespace_dir in root_path.iterdir():
                # Si no es un direcotorio, continua.
                if not namespace_dir.is_dir():
                    continue
                # Obtiene el nombre del directorio.
                namespace = namespace_dir.name
                # Para cada subcarpeta dentro.
                for model_dir in namespace_dir.iterdir():
                    # Si es un directorio.
                    if model_dir.is_dir():
                        # Añade el modelo.
                        models.append(f"{namespace}/{model_dir.name}")
            
            # Retorna los modelos.
            return models

    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"hugging_face::list_installed_models() -> [{type(e).__name__}] No se han podido listar los modelos instalados. Trace: {e}")
    
    
def install_model(model_tag:str, local_dir:Path) -> None:
    """
    Instala el modelo desde hugging face.
    
    Args:
        model_tag (str): Etiqueta del modelo.
        local_dir (Path): Path donde instalar el modelo.
    Raises:
        OSError: En caso de que haya algún error.
    """
    # Try-Except para manejo de errores.
    try:
        # Comprueba si el path es válido.
        if is_valid(root_path=local_dir):
            # Instala el modelo.
            snapshot_download(repo_id=model_tag, local_dir=os.path.join(local_dir, model_tag))

    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"hugging_face::install_model() -> [{type(e).__name__}] No se ha podido instalar el modelo. Trace: {e}")