

# ---- MÓDULOS ---- #
from pydantic import BaseModel


# ---- CLASES ---- #
class Query(BaseModel):
    """
    Query recibida del cliente.
    
    Attributes:
        session_id (str): ID de la sesión.
        content (str): Contenido de la query.
    """
    # -- Atributos -- #
    session_id:str
    content:str