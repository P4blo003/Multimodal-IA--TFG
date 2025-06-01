


# ---- MÓDULOS ---- #
from fastapi import APIRouter

from logging import Logger
from utils.logger import create_logger

from model.query import Query
from model.response import Response

from service.ollama_service import OllamaService

from config.context import CFG


# ---- VARIABLES GLOBALES ---- #
router:APIRouter = APIRouter()
logger:Logger = create_logger(logger_name=__name__, cfg=CFG.logger, console=True, file="server.log")


# ---- ENDPOINTS ---- #
@router.post('/ask')
async def ask_question(query:Query) -> Response:
    """
    Endpoint para realizar preguntas al modelo de Ollama.
    
    Args:
        query (Query): La query recibida del cliente.
    Returns:
        dict[str, any]: Diccionario con los parámetros.
    """
    logger.info(f"REC Query | CONTENT: {query.content}")        # Imprime información.
    # Envía la query al modelo de Ollama.
    response:Response = OllamaService.get_response(query.content)
    
    # Devuelve la respuesta generada.
    return response