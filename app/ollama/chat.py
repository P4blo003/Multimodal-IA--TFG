

# ---- MÓDULOS ---- #
from typing import List, Dict


# ---- CLASES ---- #
class ChatHistory:
    """
    Almacena el historial de mensajes del chat.
    
    Attributes:
        history (List[Dict[str, str]]): Lista de mensajes del chat.
        size (int): Tamaño del historial de mensajes.
    """
    def __init__(self, size:int):
        """
        Inicializa el historial de mensajes.
        
        Args:
            size (int): Tamaño del historial de mensajes.
        """
        # Inicializa las propiedades.
        self.__messages:List[Dict[str, str]] = []
        self.__maxSize:int = size
    
    # -- Propiedades -- #
    @property
    def Messages(self) -> List[Dict[str, str]]:
        """
        Devuelve el listado de mensajes.
        
        Returns:
            List[Dict[str, str]]: Lista con los mensajes.
        """
        return self.__messages
    
    # -- Métodos públicos -- #
    def add_message(self, role:str, message:str):
        """
        Añade un mensaje al historial.
        
        Args:
            role (str): Rol del mensaje ('user' o 'assistant').
            message (str): Mensaje del usuario.
        """
        # Comprueba el tamaño del historial y en caso de que sea mayor al máximo.
        if len(self.__messages) >= self.__maxSize:
            # Elimina el primer mensaje (mensahe más antiguo).
            self.__messages.pop(0)
        
        # Añade el nuevo mensaje al historial.
        self.__messages.append({'role': role, 'content': message})