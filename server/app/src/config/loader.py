# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: loader.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones para cargar configuraciones.   
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
import os
from pathlib import Path
from typing import Dict, Type, TypeVar
# Librerías externas
from pydantic import BaseModel
# Librerías internas
from utils.file import yaml as UYaml
from utils.file import common


# ---- PARÁMETROS ---- #
T = TypeVar("T", bound=BaseModel)


# ---- FUNCIONES ---- #
def load_env(file_path:Path, csys:bool=False) -> Dict[str,any]:
    """
    Carga las variables de entorno del fichero. En caso de que `csys` sea True,
    también copiara las variables de entorno del sistema.
    
    Args:
        file_path (Path): Path al fichero de variables de entorno.
        csys (bool): Indica si se deben copiar las variables de entorno
            del sistema. Por defecto es False.
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
        # Carga las variables de entorno del fichero.
        env:Dict[str,any] = common.load_env(file_path=file_path)
        
        # Comprueba si se quieren copiar las variables del sistema.
        if csys:
            # Añade las variables del sistema.
            env.update(os.environ.copy())    

        # Retorna las variables de entorno.
        return env
    
    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"loader::load_env() -> [{type(e).__name__}] No se pudo cargar las variables de entorno. Trace: {e}")

def load_config(file_path:Path, t:Type[T]) -> T:
    """
    Carga la configuración de un fichero.
    
    Args:
        file_path (Path): Ruta al fichero de configuración.
        t (Type[T]): Tipo de la clase a retornar.
    Raises:
        OSError: En caso de que ocurra algún error.
    Returns:
        T: Clase con la configuración almacenada.
    """
    # Try-Except para manejo de errores.
    try:
        # Carga los datos de un archivo:
        data = UYaml.load(file_path=file_path)
        
        # Retorna el objeto.
        return t(**data)
    
    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"loader::load_config() -> [{type(e).__name__}] No se pudo cargar los datos de configuración. Trace: {e}")