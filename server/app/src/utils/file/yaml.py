# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: yaml.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones relacionadas con el acceso, creación y eliminación
    de ficheros 'yaml'.   
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
import yaml
from pathlib import Path
# Librerías externas

# Librerías internas
from .common import is_valid


# ---- FUNCIONES ---- #
def load(file_path:Path) -> any:
    """
    Carga los datos de un fichero.
    
    Args:
        file_path (Path):
    Raises: Ruta al fichero.
        OSError: En caso de que ocurra algún error.
    Returns:
        any: Datos del fichero 'yaml'.
    """
    # Try-Except para manejo de errores.
    try:
        # Comprueba si es un fichero válido.
        if is_valid(file_path=file_path, extension='.yaml'):
            # Abre el fichero.
            with file_path.open(mode='r', encoding='utf-8') as file:
                # Carga los datos.
                data = yaml.safe_load(stream=file)
            
            # Retorna los datos.
            return data
    
    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"yaml::load() -> [{type(e).__name__}] No se pudo cargar el fichero <{file_path}>. Trace:{e}")