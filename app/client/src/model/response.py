

# ---- MÓDULOS ---- #
from pydantic import BaseModel


# ---- CLASES ---- #
class Response(BaseModel):
    """
    Respuesta a enviar al cliente.
    
    Attributes:
        session_id (str): ID de la sesión.
        statusCode (int): Estado de la respuesta.
        content (str): Contenido de la respuesta.
    """
    # -- Atributos -- #
    session_id:str
    statusCode:int = 0
    content:str