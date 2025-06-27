# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: rag.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones que permiten objetos del RAG de manera
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
from core.services.rag import RagService
from core.rag.document.base import BaseDocumentModule
from core.rag.document.haystack_module import HaystackDocumentModule
from config.schema.rag import RagConfig


# ---- FUNCIONES ---- #
def create_rag_service(ctx:ContextManager) -> RagService:
    """
    Crea y retorna un servicio de RAG.
    
    Args:
        ctx (ContextController): Gestor del contexto. Para obtener la configuración.
    Raises:
        OSError: En caso de que haya algún error.
    Returns:
        RagService: Servicio de RAG.
    """
    # Try-Except para manejo de errores.
    try:
        # Retorna el servicio.
        return RagService(rag_cfg=ctx.get_cfg('rag', t=RagConfig))

    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"rag::create_rag_service() -> [{type(e).__name__}] No se pudo crear servicio de RAG. Trace: {e}")