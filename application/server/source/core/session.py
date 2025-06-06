# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/core/session.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases relacionadas con las sesiones de chat.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from typing import List, Dict
from uuid import uuid4

from logging import Logger
from utilities.logger import create_logger

from config.schema import ChatConfig, LoggerConfig


# ---- CLASES ---- #
class ChatSession:
    """
    Clase encargada de almacenar los mensajes y respuestas de una sesión de chat.
    """
    # -- Métodos por defect -- #
    def __init__(self, max_size:int):
        """
        Inicializa la instancia.
        
        Args:
            max_size (int): Tamaño máximo del historial del chat.
        """
        # Inicializa las propiedades.
        self.__maxSize:int = max_size
        self.__chatHistory:List[Dict[str, str]] = []
    
    
    # -- Propiedades -- #
    @property
    def ChatHistory(self) -> List[Dict[str, str]]:
        """
        Devuelve el historial del chat.
        
        Returns:
            List[Dict[str,str]]: Listado con los mensajes realizados.
        """
        # Retorna el historial del chat.
        return self.__chatHistory
    

    # -- Métodos públicos -- #
    def add_message(self, role:str, content:str):
        """
        Añade un mensaje realizado por un rol al historial de la sesión.
        
        Args:
            role (str): El rol que realizo el mensaje.
            content (str): El contenido del mensaje.
        """
        # Comprueba el tamaño del historial
        if len(self.__chatHistory) >= self.__maxSize:
            self.__chatHistory.pop(0)
        
        # Añade el mensaje al historial.
        self.__chatHistory.append({'role': role, 'content': content})


class SessionController:
    """
    Clase encargada de gestionar las sesiones del servidor. Sigue el principio Singleton
    para evitar duplicaciones de la instancia.
    """
    # -- Métodos por defecto -- #   
    def __init__(self, logger_cfg:LoggerConfig):
        """
        Inicializa la instancia de la clase.
        
        Args:
            logger_cfg (LoggerConfig): Configuración del logger.
        """
        # Inicializa las propiedades.
        self.__logger:Logger = create_logger(logger_name=__name__, cfg=logger_cfg, console=True, file='server.log')
        self.__chatHistory:Dict[str, ChatSession] = {}
        
        self.__logger.info("Controlador de sesión iniciado.")   # Imprime la información.
    
    
    # -- Métodos públicos -- #
    def create_session(self, chat_cfg:ChatConfig) -> str:
        """
        Crea una sesión y devuelve el ID asociado a la misma.
        
        Args:
            chat_cfg (ChatConfig): Configuración del chat.

        Returns:
            str: ID generado por la sesión.
        """
        # Variable a devolver.
        id:str = str(uuid4())        
        # Creal la sesión de chat.
        self.__chatHistory[id] = ChatSession(max_size=chat_cfg.maxHistorySize)
        self.__logger.info(f"Sesión creada [{id}].")    # Imprime la información.
        
        # Retorna el ID generado.
        return id
    
    def get_session(self, id:str) -> ChatSession:
        """
        Devuelve la sesión de chat asociada al ID dado.
        
        Args:
            id (str): ID de la sesión de chat.
        
        Returns:
            ChatSession: Sesión de chat asociada al ID.
        """
        # Retorna la sesión
        return self.__chatHistory.get(id)