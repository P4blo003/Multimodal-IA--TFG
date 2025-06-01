

# ---- MÓDULOS ---- #
from pydantic import BaseModel


# ---- CLASES ---- #
class Query(BaseModel):
    """
    Query recibida del cliente.
    
    Attributes:
        content (str): Contenido de la query.
    """
    # -- Atributos -- #
    content:str