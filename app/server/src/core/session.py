# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/server/core/rag/session.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases relacionadas con el historial del chat
# y la sesión.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from uuid import uuid4
from typing import Dict, List

from config.context import CFG


# ---- CLASES ---- #
class ChatSession:
    """
    Clase encargada de gestionar la sesión de chat. Contiene el historial de la sesión.
    """
    # -- Métodos por defecto -- #
    def __init__(self, max_size:int):
        """
        Inicializa la instancia.
        
        Args:
            max_size (int): Tamaño máximo del historial.
        """
        # Inicializa las propiedades.
        self.__messages:List[Dict[str, str]] = []
        self.__maxSize:int = max_size
    
    # -- Métodos públicos -- #
    def add_message(self, rol:str, message:str):
        """
        Añade una chat realizado entre el usuario y el modelo.
        
        Args:
            rol (str): El rol del mensaje.
            message (str): El mensaje.
        """
        # Comprueba el tamaño del historial
        if len(self.__messages) >= self.__maxSize:
            self.__messages.pop(0)
        
        # Añade el mensaje al historial.
        self.__messages.append({'role': rol, 'content': message})
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Obtiene el historial bien formateado para añadirlo al prompt
        del usuario.

        Returns:
            List[Dict[str, str]]: Lista con los mensajes del historial.
        """
        return self.__messages
    
    
class SessionController:
    """
    Clase encargada de controlar las sesiones del modelo. Se encarga de asignar
    IDs y gestionar los chats.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la instancia.
        """
        self.__sessions:Dict[str, ChatSession] = {}
    
    # -- Métodos públicos -- #
    def get_session(self, id:str) -> ChatSession:
        """
        Obtiene la sesión a partir de un ID dado.
        
        Args:
            id (str): ID de la sesión.
        Returns:
            ChatSession: La sesión de chat relacionada con el ID.
        """
        # Retorna la sesión.
        return self.__sessions.get(id)
    
    def create_session(self) -> str:
        """
        Crea una nueva sesión.
        
        Returns:
            str: El ID generado.
        """
        # Variable a devolver.
        id:str = str(uuid4())
        
        # Creal la sesión de chat.
        self.__sessions[id] = ChatSession(max_size=CFG.chat.maxHistorySize)
        
        # Retorna el ID generado.
        return id