# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: path.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones relacionadas con rutas del sistema.   
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

# Librerías internas


# ---- FUNCIONES ---- #
def is_valid(root_path:Path) -> bool:
    """
    Comrpueba si el path es un directorio válido.
    
    Args:
        root_path (Path): Path a comprobar.
    Rasies:
        FileNotFoundError: En caso de que el directorio no exista.
        ValueError: En caso de que el path no sea un directorio.
    Returns:
        bool: True si el directorio es válido.
    """
    # Comprueba si el directorio existe.
    if not root_path.exists():
        # Lanza una excepción.
        raise FileNotFoundError(f"path::is_valid() -> No existe el path <{root_path}>.")
    
    # Comprueba si no es un directorio.
    if not root_path.is_dir():
        # Lanza una excepción.
        raise ValueError(f"path::is_valid() -> El path <{root_path}> no es un directorio.")
    
    # Retorna true.
    return True
    
def list_dir_files(root_path:Path, recursive:bool) -> List[str]:
    """
    Lista el directorio dado, devolviendo los ficheros que contiene. En caso de que recursive sea True
    se listarna también los subdirectorios de manera recursiva.
    
    Args:
        root_path (Path): Directorio raiz.
        recursive (bool): Si se desea listar los subdirectorios dentro del directorio raiz.
    Raises:
        OSError: En caso de que haya algún error.
    Returns:
        List[str]: Listado con los ficheros.
    """
    # Try-Except para manejo de excepciones.
    try:
        # Crea el Path.
        base_path = Path(root_path)

        # Comprueba que el directorio es válido.
        if is_valid(root_path=root_path):

            # Elige el iterador adecuado: recursivo o no.
            paths = base_path.rglob('*') if recursive else base_path.glob('*')
            
            # Filtra archivos según extensión si aplica.
            files = [str(p.resolve()) for p in paths if p.is_file()]

            # Retorna los ficheros.
            return files
    
    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"path::list_dir_files() -> [{type(e).__name__}] No se ha podido listar el directorio <{root_path}>. Trace: {e}")

def list_dir_folders(root_path:Path) -> list[str]:
    """
    Lista las carpetas dentro de un dictorio dado.
    
    Args:
        root_path (Path): Directorio a listar.
    Raises:
        OSError: En caso de que haya algún error.
    Returns:
        List[str]: Listado con las carpetas.
    """
    # Try-Except para manejo de errores.
    try:
        # Comprueba si el directorio es válido.
        if is_valid(root_path=root_path):
            # Lista el directorio.
            subdirs = [dir.name for dir in root_path.iterdir() if dir.is_dir()]
            
            # Retorna los subdirectorios.
            return subdirs
    
    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"path::list_dir_folders() -> [{type(e).__name__}] No se ha podido listar el directorio. Trace: {e}")

def create_root_path(root_path:str, filename:str, exist_ok:bool=True, recursive:bool=True) -> Path:
    """
    Crea la ruta donde se creara el fichero y devuelve la ruta completa (junto con el fichero). Si el el valor de
    `recursive` es True, crea todas las carpetas hasta el fichero. En caso contrario lanzara
    una excepción en caso de que el directorio no exista.
    Si el fichero ya existe, se lanzará una excepción si el valor de `exist_ok` es False.
    
    Args:
        root_path (str): Path del directorio donde crear el fichero.
        filename (str): Nombre del fichero a crear.
        exist_ok (bool): Si se debe lanzar excepción en caso de que el archivo ya exista.
        recursive (bool): Si se deben crear las carpatas hasta el fichero.
    
    Raises:
        FileNotFoundError: En caso de que el directorio no exista y `recursive` sea False.
        Exception: Cualquier error que no sea FileNotFoundError y sea causado por errores
            de sistema.
        
    Returns:
        Path: Path completo del fichero.
    """
    # Genera el Path
    root_path = Path(root_path)

    # Comprueba si no se deben crear las carpetas y si no existe el directorio.
    if not recursive and not root_path.exists():
        # Lanza una excepción.
        raise FileNotFoundError(f"No existe el directorio: {root_path}. Establecer 'recursive' como True para crear las carpetas.")

    # Crea la ruta completa.
    completePath:Path = Path(os.path.join(root_path, filename))
    
    # Comprueba si el directorio no existe.
    if not root_path.exists():
        # Crea todas las carpetas.
        os.makedirs(os.path.dirname(completePath), exist_ok=exist_ok)
    