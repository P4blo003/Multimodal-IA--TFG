# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: ollama.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones que permiten crear objetos de Ollama de manera
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
from core.services.ollama import OllamaService
from config.schema.ollama import OllamaConfig


# ---- FUNCIONES ---- #
def create_ollama_service(ctx:ContextManager) -> OllamaService:
    """
    Crea y retorna un servicio de Ollama.
    
    Args:
        ctx (ContextController): Gestor del contexto. Para obtener la configuración.
    Raises:
        OSError: En caso de que haya algún error.
    Returns:
        OllamaService: Servicio de Ollama.
    """
    # Try-Except para manejo de errores.
    try:
        # Retorna el servicio.
        return OllamaService(service_cfg=ctx.get_cfg('ollama', t=OllamaConfig).service)

    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"ollama::create_ollama_service() -> [{type(e).__name__}] No se pudo crear servicio Ollama. Trace: {e}")