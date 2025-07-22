# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: conversation_manager.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones que se encargan de gestionar las
    comversaciones. Recibe la consulta, genera el prompt y lo envía al modelo.    
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
from typing import List, Dict
# Librerías externas

# Librerías internas
from model.context import ContextDTO
from context.context_manager import ContextManager
from core.services.ollama import OllamaService
from core.services.rag import RagService
from core.services.prompt import PromptService


# ---- CLASES ---- #
class ConversationManager:
    """
    Gestiona la conversación con el modelo.
    """
    # -- Métodos por defecto -- #
    def __init__(self, ctx:ContextManager):
        """
        Inicializa las propiedades.
        
        Args:
            ctx (ContextManager): Gestor del contexto.
        """
        # Inicializa las propiedades.
        self.__ctx:ContextManager = ctx
        self.__maxSize:int = 20
        self.__chatHistory:List[Dict[str, str]] = []
    
    # -- Métodos privados -- #
    def __add_message(self, role:str, content:str):
        """
        Añade un mensaje realizado por un rol al historial de la sesión.
        
        Args:
            role (str): El rol que realizo el mensaje.
            content (str): El contenido del mensaje.
        Raises:
            OSError: En caso de que haya algún error.
        """
        # Try-except para el manejo de errores.
        try:
            # Comprueba el tamaño del historial
            if len(self.__chatHistory) >= self.__maxSize:
                self.__chatHistory.pop(0)
            
            # Añade el mensaje al historial.
            self.__chatHistory.append({'role': role, 'content': content})
        
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"ConversationManager.__add_message() -> [{type(e).__name__}] No se pudo añadir mensaje al historial. Trace: {e}")
        
    # -- Métodos públicos -- #
    def chat(self, query:str) -> str:
        """
        Genera el prompt a partir de la consulta, el contexto y el historial. Envía el prompt
        al modelo de Ollama y recibe la respuesta.
        
        Args:
            query (str): Query realizada por el usuario.
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            str: Respuesta del modelo.
        """
        # Try-Except para el manejo de excepciones.
        try:
            # TODO: Preprocesar la query.

            # Genera los embeddings.
            self.__ctx.get_service(key='rag', t=RagService).make_embeddings()
            
            # Obtener el contexto.
            context:List[ContextDTO] = self.__ctx.get_service(key='rag', t=RagService).get_relevant_context(query=query)
            
            # Generar el prompt.
            prompt:str = self.__ctx.get_service(key='prompt', t=PromptService).build_prompt(
                context=context,
                history=self.__chatHistory,
                query=query
            )

            # Envia el prompt y obtiene la respuesta.
            resp:str =  self.__ctx.get_service(key='ollama', t=OllamaService).get_response(prompt=prompt)
            
            # Almacena la pregunta/respuesta en el historial.
            self.__add_message(role='user', content=query)
            self.__add_message(role='assistant', content=resp)
            
            # Retorna la respuesta.
            return resp
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"ConversationManager.chat() -> [{type(e).__name__}] No se pudo conversar con el modelo. Trace: {e}")