# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/src/utils/process.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene funciones relacionadas con la creación de procesos.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
from subprocess import Popen
from pathlib import Path


# ---- FUNCIONES ---- #
def start_subprocess(args, env:dict=None, file:Path=None) -> Popen:
    """
    Inicializa el subproceso.
    
    Args:
        args: Argumentos del subproceso.
        anv (dict): Variables de entorno.
        file (Path): Ruta al archivo de salida.

    Returns:
        Popen: Subproceso creado.
    """
    if file:
        # Inicia el subproceso.
        with file.open('w', encoding='utf-8') as file:
            # Si se han pasado variables de entorno para el subproceso.
            if env:
                process:Popen = Popen(
                    args=args,
                    env=env,
                    stdout=file,
                    stderr=file
                )
            else:
                process:Popen = Popen(
                    args=args,
                    stdout=file,
                    stderr=file
                )
    else:
        # Inicia el subproceso.
        with open(os.devnull, 'w', encoding='utf-8') as devnull:
            # Si se han pasado variables de entorno para el subproceso.
            if env:
                process:Popen = Popen(
                    args=args,
                    env=env,
                    stdout=devnull,
                    stderr=devnull
                )
            else:
                process:Popen = Popen(
                    args=args,
                    stdout=devnull,
                    stderr=devnull
                )
    
    # Devuelve el subproceso.
    return process