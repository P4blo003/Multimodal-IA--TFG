# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/ollama/client.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene la clase OllamaClient, que se encarga de 
# interactuar con el modelo de Ollama.
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import logging
from utils.log.logger import get_logger

import requests

from . import install_model
from .response import process_response
from .classes import Response, ChatHistory

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
        self.__apiBaseUrl:str = f"http://{self.__cfg.host}:{self.__cfg.port}"
        self.__chatHistory:ChatHistory = ChatHistory(self.__cfg.chatHistorySize)  # Inicializa el historial de mensajes.
        
        self.__logger:logging.Logger = get_logger(name=__name__, file="app.log", file_only=True)    # Crea el logger de la clase.
        
        self.__checkModel()  # Comprueba si el modelo está disponible.
        self.__logger.info("Iniciado cliente de Ollama.")
    
    # -- Métodos privados -- #
    def __checkModel(self):
        """
        Comprueba si el modelo está disponible. En caso de que no lo esté, lo intenta instalar.
        """
        # Genera la URL.
        url:str = f"{self.__apiBaseUrl}/api/tags"
        # Imprime información del mensaje.
        self.__logger.info(f"TO: {url} | GET | LIST_MODELS")
        try:
            # Intenta hacer una petición al servidor.
            response = requests.get(url)
            response.raise_for_status()  # Lanza un error si la respuesta no es 200
            # Obtiene la respuesta en formato JSON.
            models = response.json().get("models", [])
            # Comrpueba si existe algún modelo.
            exist = any(model.get("name", "").startswith(self.__cfg.model) for model in models)
            # Si no existe, lo instala:
            if not exist:
                self.__logger.warning(f"Modelo ({self.__cfg.model}) no instalado.")
                try:
                    install_model(self.__cfg.bin, model=self.__cfg.model)  # Instala el modelo.
                    self.__logger.info(f"Modelo ({self.__cfg.model}) instalado.")
                except Exception as e:
                    self.__logger.error(f"Error al instalar el modelo: {e}")
                    pass
        # En caso de que haya alguna excepción.
        except Exception as e:
            self.__logger.error(f"Error al enviar el mensaje: {e}")
            return None

    # -- Métodos públicos -- #
    def send_message(self, message:str) -> Response:
        """
        Envía un mensaje al modelo de Ollama y devuelve la respuesta.
        
        Args:
            message (str): Mensaje a enviar al modelo.
        
        Returns:
            Response: Respuesta del modelo.
        """
        # Añade el mensaje al historial.
        self.__chatHistory.add_message(role="user", message=message)
        # Genera la URL:
        url:str = f"{self.__apiBaseUrl}/api/generate"
        # Genera los datos a enviar al servicio ollama.
        payload = {
            "model": self.__cfg.model,
            **self.__chatHistory.get_payload(),
            "stream": False
        }
        # Imprime información del mensaje.
        self.__logger.info(f"TO: {url} | CONTENT: {payload}")
        try:
            # Intenta hacer una petición al servidor.
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Lanza un error si la respuesta no es 200
            # Obtiene la respuesta en formato JSON.
            reply = response.json()
            fmt_response = process_response(reply)  # Procesa la respuesta.
            # Si se ha procesado la respuesta correctamente.
            if fmt_response:
                # Añade el mensaje al historial.
                self.__chatHistory.add_message(role="assistant", message=fmt_response.response)
                self.__logger.info(f"FROM: {url} | RESPONSE: {fmt_response.response} | PROMPT_TOKENS: {fmt_response.tokens_prompt} | GEN_TOKENS: {fmt_response.generated_tokens} | TOTAL_TIME: {fmt_response.total_time} s.")  # Imprime la respuesta.
            # Retorna la respuesta formateada.
            return fmt_response
        
        # En caso de que haya alguna excepción.
        except Exception as e:
            self.__logger.error(f"Error al enviar el mensaje: {e}")
            return None
    
    