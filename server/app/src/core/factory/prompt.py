# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: prompt.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones que permiten crear prompts de manera
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
from core.services.prompt import PromptService
from config.schema.prompt import PromptConfig


# ---- FUNCIONES ---- #
def create_prompt_service(ctx:ContextManager) -> PromptService:
    """
    Crea y retorna un servicio de prompts.
    
    Args:
        ctx (ContextController): Gestor del contexto. Para obtener la configuración.
    Raises:
        OSError: En caso de que haya algún error.
    Returns:
        PromptService: Servicio de prompts.
    """
    # Try-Except para manejo de errores.
    try:
        # Retorna el servicio.
        return PromptService(prompt_cfg=ctx.get_cfg('prompt', t=PromptConfig))

    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"prompt::create_prompt_service() -> [{type(e).__name__}] No se pudo crear servicio de prompts. Trace: {e}")