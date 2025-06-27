# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: uvicorn.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones que permiten crear objetos de Uvicorn de manera
    más sencilla.  
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar

# Librerías externas

# Librerías internas
from context.context_manager import ContextManager
from core.services.uvicorn import UvicornService
from config.schema.uvicorn import UvicornConfig


# ---- FUNCIONES ---- #
def create_uvicorn_service(ctx:ContextManager) -> UvicornService:
    """
    Crea y retorna un servicio de Uvicorn.
    
    Args:
        ctx (ContextController): Gestor del contexto. Para obtener la configuración.
    Raises:
        OSError: En caso de que haya algún error.
    Returns:
        UvicornService: Servicio de Uvicorn.
    """
    # Try-Except para manejo de errores.
    try:
        # Retorna el servicio.
        return UvicornService(uvicorn_cfg=ctx.get_cfg('uvicorn', t=UvicornConfig))

    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"uvicorn::create_uvicorn_service() -> [{type(e).__name__}] No se pudo crear servicio Uvicorn. Trace: {e}")