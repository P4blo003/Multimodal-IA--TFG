# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/chat/history.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene las clases encargadas degestionar el historial
# del chat.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from typing import List, Dict


# ---- CLASES ---- #
class ChatHistory:
    """
    Instancia que se encarga de almacenar el historial del chat.
    """
    # -- Métodos por defecto -- #
    def __init__(self, max_history_size:int):
        """
        Inicializa la instancia.
        
        Args:
            max_history_size (int): Tamaño máximo del historial.
        """
        # Inicializa las propiedades.
        self.__maxHistorySize:int = max_history_size
        self.__buffer:List[Dict[str, str]] = []
    
    # -- Métodos públicos -- #
    def Add(self, role:str, message:str) -> any:
        """
        Añade una chat realizado entre el usuario y el modelo.
        """
        # Comrpueba el tamaño del historial.
        if len(self.__buffer) >= self.__maxHistorySize: # Si el tamaño es mayor o igual al máximo
            self.__buffer.pop(0)    # Elimina el primer mensaje (el más alejado temporalmente).
        
        # Añade el nuevo mensaje.
        self.__buffer.append({'role': role, 'content': message})
    
    def GetHistory(self) -> List[Dict[str, str]]:
        """
        Obtiene el historial bien formateado para añadirlo al prompt
        del usuario.
        
        Returns:
            List[Dict[str, str]]: Lista con los mensajes del historial.
        """
        return self.__buffer