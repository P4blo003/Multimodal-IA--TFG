# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: common.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones comunes relacionadas con los ficheros. 
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
import os
from pathlib import Path
from typing import Dict
# Librerías externas
from dotenv import dotenv_values
# Librerías internas


# ---- FUNCIONES ---- #
def is_valid(file_path:Path, extension:str=None) -> bool:
    """
    Comprueba si el fichero es válido. Es decir si existe, es un fichero
    y además tiene la extensión esperada.
    
    Args:
        file_path (Path): Ruta al fichero.
        extension (str): Extensión del fichero.
    Raises:
        FileNotFoundError: Si el fichero no existe.
        ValueError: Si no es un fichero válido.
    Returns:
        bool: True si es un fichero válido.
    """
    # Comprueba si el fichero existe.
    if not file_path.exists():
        # Lanza una excepción.
        raise FileNotFoundError(f"file::common.is_valid() -> No existe el path <{file_path}>.")
    
    # Comprueba no es un fichero.
    if  file_path.is_dir():
        # Lanza una excepción.
        raise OSError(f"file::common.is_valid() -> El path <{file_path}> no es un fichero.")
    
    # Si se quiere comprobar la extensión.
    if extension:
        # Obtiene la extensión del fichero.
        __, file_extension = os.path.splitext(file_path)
        # Comprueba si no es la extensión esperada.
        if file_extension.lower() != extension.lower():
            # Lanza una excepción.
            raise OSError(f"file::common.is_valid() -> El path <{file_path}> no tiene la extensión esperada <{extension}>.")
    
    # Retorna True
    return True

def load_env(file_path:Path) -> Dict[str,any]:
    """
    Carga las variables de entorno de un fichero.
    
    Args:
        file_path (Path): Path al fichero de variables de entorno.
    Raises:
        FileNotFoundError: En caso de que el fichero no exista.
        ValueError: En caso de que el PATH sea incorrecto:
            - No es un fichero.
        OSError: En caso de cualquier error excepto `FileNotFoundError`.
    Returns:
        Dict[str,any]: Diccionario con las variables de entorno.
    """
    # Try-Except para manejo de errores.
    try:
        # Comprueba si el fichero no existe.
        if is_valid(file_path=file_path):
            # Retorna las variables de entorno del fichero.
            return dotenv_values(dotenv_path=file_path)

    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"common::load_env() -> [{type(e).__name__}] No se pudo cargar el fichero <{file_path}>. Trace:{e}")