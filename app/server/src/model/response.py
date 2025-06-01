

# ---- MÓDULOS ---- #
from pydantic import BaseModel


# ---- CLASES ---- #
class Response(BaseModel):
    """
    Respuesta a enviar al cliente.
    
    Attributes:
        content (str): Contenido de la respuesta.
        statusCode (int): Estado de la respuesta.
        loadDuration (Optional[float]): Duración total en cargar el modelo, en segundos.
        promptEvalDuration (Optional[float]): Tiempo empleado en evaluar el prompt, en segundos.
        responseGenDuration (Optional[float]): Duración total en generar la respuesta, en segundos.
        promptTokens (Optional[int]): Número de tokens en el prompt.
        responseTokens (Optional[int]): Número de tokens en la respuesta.
        speed (Optional[float]): Velocidad de generación de la respuesta, en tokens/segundo.
    """
    # -- Atributos -- #
    content:str
    statusCode:int = 0
    loadDuration:float = 0.0
    promptEvalDuration:float = 0.0
    responseGenDuration:float = 0.0
    promptTokens:int = 0
    responseTokens:int = 0
    speed:float = 0.0