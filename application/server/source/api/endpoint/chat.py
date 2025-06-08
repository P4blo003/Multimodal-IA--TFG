# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/api/endpoint/chat.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene los endpoints del chat del servidor.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from model.query import QueryDTO
from model.response import ResponseDTO

from logging import Logger
from utilities.logger import create_logger

from core.session import SessionController, ChatSession
from core.conversation import ConversationController
from core.dependencies import get_session_controller, get_conversation_controller

from config.context import CFG


# ---- VARIABLES GLOBALES ---- #
logger:Logger = create_logger(logger_name=__name__, cfg=CFG.logger, console=True, file='server.log')
router:APIRouter = APIRouter()


# ---- ENDPOINTS ---- #
@router.get('/init')
async def get_id(session_controller:SessionController = Depends(get_session_controller)) -> ResponseDTO:
    """
    Solicita al servidor un ID de sesión. El servidor inicializa
    una sesión para el ID dado.
    
    Args:
        session_controller (SessionController): Controlador de sesión.
    
    Raises:
        HTTPException: Causada cuando ocurre algún error durante la ejecución del endpoint.

    Returns:
        ResponseDTO: Respuesta generada por el servidor.
    """
    # Try-Except para manejo de excepciones.
    try:
        # Crea la sesión.
        id:str = session_controller.create_session(chat_cfg=CFG.chat)
        # Crea la respuesta.
        resp:ResponseDTO = ResponseDTO(session_id=id, content="")
        # Crea la respuesta.
        return resp

    # Si ocurre cualquier excepción.
    except Exception as e:
        logger.error(e)         # Imprime el error.
        # Lanza una excepción.
        raise HTTPException(status_code=500, detail='Error interno en el servidor')     # Lanza la excepción.

@router.post('/question/{session_id}')
async def make_question(session_id:str, query:QueryDTO,
                        session_controller:SessionController = Depends(get_session_controller),
                        conversation_controller:ConversationController = Depends(get_conversation_controller)) -> ResponseDTO:
    """
    Recibe la query del usuario a partir de un método POST, genera la respuesta
    y devuelve el valor obtenido.
    
    Args:
        session_id (str): ID de la sesión del chat.
        query (QueryDTO): Datos recibidos por el servidor.
        session_controller (SessionController): Controlador de sesión.
        conversation_controller (ConversationController): Controlador de la conversación.
    
    Raises:
        HTTPException: Causada cuando ocurre algún error durante la ejecución del endpoint.

    Returns:
        ResponseDTO: Respuesta generada por el servidor.
    """
    # Try-Except para manejo de excepciones.
    try:
        # Obtiene la sesión en función del ID dado.
        session:ChatSession = session_controller.get_session(id=session_id)
        
        # Comprueba si existe una sesión para el ID.
        if not session:     # Si no se encontró ninguna sesión.
            # Lanza una excepción.
            raise HTTPException(status_code=401, detail='ID de sesión no reconocido.')
        
        # Obtiene la respuesta del modelo.
        resp_content:str = conversation_controller.chat(query=query.content, chat_session=session, ollama_api_cfg=CFG.ollama.api)
        
        # Retorna la respuesta.
        return ResponseDTO(session_id=session_id, content=resp_content)

    # Si ocurre alguna excepción HTTPException.
    except HTTPException as e:
        logger.error(e)         # Imprime el error.
        # Lanza la misma excepción.
        raise e

    # Si ocurre cualquier excepción.
    except Exception as e:
        logger.error(e)         # Imprime el error.
        # Lanza una excepción.
        raise HTTPException(status_code=500, detail='Error interno en el servidor')