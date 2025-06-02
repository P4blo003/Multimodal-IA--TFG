


# ---- MÓDULOS ---- #
from fastapi import APIRouter

from logging import Logger
from utils.logger import create_logger

from model.query import Query
from model.response import Response

from core.session import SessionController, ChatSession
from core.conversation import ConversationController

from config.context import CFG


# ---- VARIABLES GLOBALES ---- #
router:APIRouter = APIRouter()
logger:Logger = create_logger(logger_name=__name__, cfg=CFG.logger, console=True, file="server.log")
session_controller:SessionController = SessionController()
conversation_controller:ConversationController = ConversationController(cfg=CFG)


# ---- ENDPOINTS ---- #
@router.get('/init')
async def get_id() -> Response:
    """
    Solicita al servidor un ID de sesión para el chat.
    
    Returns:
        Response: Respuesta con el id de la sesión.
    """
    # Variable a devolver.
    response:Response = None

    # Try-except para manejo de excepciones.
    try:
        # Crea la nueva sesión.
        id:str = session_controller.create_session()
        logger.info(f"Session created | ID: {id}")      # Imprime la información.
        # Crea la respuesta.
        response = Response(session_id=id, statusCode=200, content="")
    
    # Si ocurre alguna excepción.
    except Exception as e:
        logger.error(e)
        # Crea la respuesta.
        response = Response(session_id="", statusCode=500, content="")      # Imprime el error.
    
    # Retorna la respuesta generada.
    return response

@router.post('/ask')
async def ask_question(query:Query) -> Response:
    """
    Endpoint para realizar preguntas al modelo de Ollama.
    
    Args:
        query (Query): La query recibida del cliente.
    Returns:
        Response: Respuesta del servidor.
    """
    # Variable con la sesión.
    session:ChatSession | None = session_controller.get_session(id=query.session_id)   # Obtiene la sesión del ID.
    
    # Comprueba que se haya obtenido la sesión.
    if not session:
        logger.warning(f"[Sesión no encontrada] | ID: {query.session_id}")  # Imprime el aviso.
        return Response(session_id="", statusCode=401, content="ID de sesión inválido.")

    logger.info(f"[Sesión activa] | ID: {query.session_id}")                # Imprime la información.
    logger.info(f"[Consulta recibida] | QUERY: {query.content}")            # Imprime la información.
    
    response:Response = conversation_controller.get_response(query=query.content, session=session)              # Obtiene la respuesta.
    
    # Si la respuesta es correcta.
    if response.statusCode == 200:
        # Guarda el intercambio en el historial.
        session.add_message(rol='user', message=query.content)
        session.add_message(rol='assistant', message="")
    
    # Devuelve la respuesta generada.
    return response