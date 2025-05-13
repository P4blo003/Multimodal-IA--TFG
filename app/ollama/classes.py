# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/utils/log/classes.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases relacionadas con ollama.
# -----------------------------------------------------------------------------

# ---- Módulos ---- #
from dataclasses import dataclass

from typing import List, Dict

# ---- Clases de datos ---- #
@dataclass
class OllamaConfig:
    """
    Clase que almacena la configuración de ollama.
    
    Attributes:
        host (str): Host del servicio de ollama.
        port (int): Puerto del servicio de ollama.
        bin (str): Ruta al fichero binario de ollama.
        silent (bool): Si se debe mostrar los mensajes de ollama.
        file (str): Ruta al fichero de logs.
        model (str): Nombre del modelo de ollama.
        chatHistorySize (int): Tamaño del historial de mensajes.
        startupWaitTime (int): Tiempo de espera para que el servidor esté listo.
    """
    # -- Parámetros -- #
    host:str = '0.0.0.0'
    port:int = 11434
    bin:str = 'bin/ollama/ollama'
    silent:bool = False
    file:str = 'logs/ollama_serve.log'
    model:str = 'llama3.1'
    chatHistorySize:int = 10
    startupWaitTime:int = 5

@dataclass
class Response:
    """
    Almacena la respuesta del modelo de Ollama.
    
    Attributes:
        mdel (str): Nombre del modelo.
        response (str): Respuesta del modelo.
        tokens_prompt (int): Número de tokens del prompt.
        generated_tokens (int): Número de tokens generados.
        total_time (float): Tiempo total de la petición.
        load_model_time (float): Tiempo de carga del modelo.
        eval_prompt_time (float): Tiempo de evaluación del prompt.
        generation_time (float): Tiempo de generación de la respuesta.
    """
    # -- Parámetros -- #
    model:str = None
    response:str = None
    tokens_prompt:int = None
    generated_tokens:int = None
    total_time:float = None
    load_model_time:float = None
    eval_prompt_time:float = None
    generation_time:float = None

# ---- Clases ---- #
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