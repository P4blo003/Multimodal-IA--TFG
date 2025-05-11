# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/ollama/client.py
# Autor: Pablo González García
# Descripción: 

# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import logging
from utils.log.logger import get_logger

import requests

from .response import process_response
from .classes import Response

from config.context import OLLAMA_CFG

# ---- Clases ---- #
class OllamaClient:
    """
    Cliente para interactuar con un modelo de Ollama vía HTTP.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa el cliente de Ollama.
        """
        self.__cfg = OLLAMA_CFG
        self.__apiUrl:str = f"http://{self.__cfg.host}:{self.__cfg.port}/api/generate"
        
        self.__logger:logging.Logger = get_logger(name=__name__, file="app.log", file_only=True)    # Crea el logger de la clase.
        
        self.__logger.info("Iniciado cliente de Ollama.")
    
    # -- Métodos públicos -- #
    def send_message(self, message:str) -> Response:
        """
        Envía un mensaje al modelo de Ollama y devuelve la respuesta.
        
        Args:
            message (str): Mensaje a enviar al modelo.
        
        Returns:
            Response: Respuesta del modelo.
        """
        # Genera los datos a enviar al servicio ollama.
        payload = {
            "model": self.__cfg.model,
            "prompt": message,
            "stream": False
        }
        # Imprime información del mensaje.
        self.__logger.info(f"TO: {self.__apiUrl} | CONTENT: {payload}")
        try:
            # Intenta hacer una petición al servidor.
            response = requests.post(self.__apiUrl, json=payload)
            response.raise_for_status()  # Lanza un error si la respuesta no es 200
            # Obtiene la respuesta en formato JSON.
            reply = response.json()
            fmt_response = process_response(reply)  # Procesa la respuesta.
            # Si se ha procesado la respuesta correctamente.
            if fmt_response:
                self.__logger.info(f"FROM: {self.__apiUrl} | RESPONSE: {fmt_response.response} | PROMPT_TOKENS: {fmt_response.tokens_prompt} | GEN_TOKENS: {fmt_response.generated_tokens} | TOTAL_TIME: {fmt_response.total_time} s.")  # Imprime la respuesta.
            # Retorna la respuesta formateada.
            return fmt_response
        
        # En caso de que haya alguna excepción.
        except Exception as e:
            self.__logger.error(f"Error al enviar el mensaje: {e}")
            return None
    
    