

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
    
    def get_payload(self) -> List[Dict[str, str]]:
        """
        Devuelve el historial de mensajes en el formato adecuado para la API.
        
        Returns:
            List[Dict[str, str]]: Historial de mensajes.
        """
        prompt = "\n".join(
            f"{m['role']}: {m['content']}" for m in self.__messages
        )
        return {"prompt":prompt}