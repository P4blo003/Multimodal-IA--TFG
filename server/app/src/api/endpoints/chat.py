# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: chat.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene los endpoints de chat del servidor.   
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
from typing import cast
from logging import Logger
# Librerías externas
from fastapi import APIRouter, HTTPException
from fastapi import Depends
# Librerías internas
import context.singleton as CtxSingleton
from context.context_manager import ContextManager
from model.query import BaseQueryDTO
from model.response import BaseResponseDTO
from core.conversation.conversation_manager import ConversationManager
from utils import console


# ---- PARÁMETROS ---- #
__ROUTER:APIRouter = APIRouter()
__CONVERSATION_MANAGER:ConversationManager = ConversationManager(ctx=CtxSingleton.get_ctx())


# ---- FUNCIONES ---- #
@__ROUTER.post('')
async def get_response(query:BaseQueryDTO) -> BaseResponseDTO:
    """
    Solicita una respuesta al modelo de Ollama a partir de la consulta del usuario.
    
    Args:
        query (BaseQueryDTO): Contiene la información de la consulta del cliente.
    Raises:
        HTTPException: En caso de que haya algún error.
    Returns:
        BaseResponseDTO: Respuesta generada por el modelo de Ollama.
    """
    # Try-Except para manejo de errores.
    try:
        # Obtiene la respuesta del modelo
        response:str = __CONVERSATION_MANAGER.chat(query=query.content)
        
        # Retorna la respuesta generada.
        return BaseResponseDTO(content=response)
    
   # Si ocurre algún error.     
    except Exception as e:
        # Imprime información.
        console.print_message(message=f'chat::get_response() -> [{type(e).__name__}] No se pudo obtener respuesta. Trace: {e}',
                              type=console.MessageType.ERROR)
        # Lanza una excepción.
        raise HTTPException(status_code=500, detail='Internal Server Error.')
