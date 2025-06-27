# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: singleton.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones que permiten inicializar una única vez
    las instancias (singleton) y poder acceder a ellas desde cualquier parte del código.    
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar

# Librerías externas

# Librerías internas
from .context_manager import ContextManager


# ---- PARÁMETROS ---- #
__CTX:ContextManager = None


# ---- FUNCIONES ---- #
def init() -> None:
    """
    Inicializa todas las clases.
    
    Raises:
        OSError: En caso de que haya algun error.
    """
    # Variables globales.
    global __CTX
    
    # Try-Except para manejo de errores.
    try:
        # Comprueba si no está inicializado.
        if not __CTX:
            # Lo inicializa.
            __CTX = ContextManager()

    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"singleton::init() -> [type(e).__name__] No se pudo inicialiar el contexto. Trace: {e}")

def get_ctx() -> ContextManager:
    """
    Retorna el gestor del contexto.
    
    Returns:
        ContextManager: Gestor del contexto.
    """
    # Variables globales.
    global __CTX
    
    # Retorna el gestor del contexto.
    return __CTX