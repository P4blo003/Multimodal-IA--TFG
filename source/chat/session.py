# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/chat/session.py
# Autor: Pablo González García
# Descripción:
# Módulo con clases y funciones relacionadas con la sesion de chat con el
# modelo.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from logging import Logger
from common.logger import create_logger

from external.ollama.net import generate_chat_response
from external.ollama.net import OllamaResponse

from .history import ChatHistory

from backend.manager import BackendManager
from backend.haystack.manager import HaystackManager
from backend.langchain.manager import LangChainManager

from yaspin import yaspin

from config.context import CFG


# ---- CLASES ---- #
class ChatSession:
    """
    Instancia que representa una sesión de chat y se encarga de gestionar todas
    las funciones relacionadas con consultas.
    """
    # -- Métodos por defecto -- #
    def __init__(self, ollama_url:str):
        """
        Inicializa la instancia.
        
        Args:
            ollama_url (str): Url del servicio de Ollama.
        """
        # Inicializa las propiedades.
        self.__logger:Logger = create_logger(logger_name=__name__, console=False, file="app.log")
        self.__ollamaUrl:str = ollama_url
        self.__chatHistory:ChatHistory = ChatHistory(max_history_size=CFG.chat.maxHistorySize)
        self.__backendManager:BackendManager = None
        # Inicializa el backend en función del parámetro de configuración.
        """
        match (CFG.rag.backend):
            case 'HAYSTACK':
                self.__backendManager = HaystackManager()
            case 'LANGCHAIN':
                self.__backendManager = LangChainManager()    
        """                    
    
    # -- Métodos privados -- #
    def __print_response_info(self, response:OllamaResponse) -> any:
        """
        Imprime los parámetros de la respuesta en el log.
        
        Args:
            response (OllamaResponse): Clase con los datos de la respuesta.
        """
        # Imprime los datos.
        self.__logger.info(F"RESPONSE\t\tRESPONSE: {response.response}")
        self.__logger.info(F"RESPONSE\t\tLOAD_DURATION: {response.loadDuration} s")
        self.__logger.info(F"RESPONSE\t\tPROMPT_EVAL_DURATION: {response.promptEvalDuration} s")
        self.__logger.info(F"RESPONSE\t\tRESPONSE_GEN_DURATION: {response.responseGenDuration} s")
        self.__logger.info(F"RESPONSE\t\tPROMPT_TOKENS: {response.promptTokens}")
        self.__logger.info(F"RESPONSE\t\tRESPONSE_TOKENS: {response.responseTokens}")
        self.__logger.info(F"RESPONSE\t\tSPEED: {response.speed} tokens/s")
    
    # -- Métodos públicos -- #
    def StartChat(self) -> any:
        """
        Inicializa el chat.
        """        
        # Try-except para posibles excepciones o Ctrl+C.
        try:
            # Búcle infinito para el chat.
            while True:
                # Obtiene el input del usuario.
                __userInput:str = input("🧠 (usuario):")
                print()         # Imprime salto de línea.
    
                # Comprueba si es un comando de salida.
                if __userInput.upper() in CFG.chat.exitCommands:
                    self.__logger.info(f"Comando de salida detectado. VALUE: {__userInput}")    # Imprime información.
                    break       # Finaliza el bucle.
                
                # Si no es un comando de salida.
                self.__logger.info(F"Mensaje del usuario. QUERY: {__userInput}")    # Imprime información.
                
                # __prompt:str = self.__backendManager.BuildPrompt(user_input=__userInput, history=self.__chatHistory)
                
                # Obtiene la respuesta del servicio Ollama.
                with yaspin(text="Generando respuesta ...") as sp:
                    __response:OllamaResponse = generate_chat_response(ollama_url=self.__ollamaUrl, model_name=CFG.model.name, prompt=__userInput)

                # Imprime la información de la respuesta.
                self.__logger.info(f"RESPONSE\t\tSTATUS_CODE: {__response.statusCode}")
                
                # Comprueba si la respuesta ha sido correcta.
                if __response.statusCode != 200:                # Si la respuesta no ha sido correcta.
                    continue                                    # Salta la iteración del búcle.
                
                # Si la respuesta ha sido correcta: 200.
                self.__chatHistory.Add(role='user', message=__userInput)                # Añade la query del usuario al historial.
                self.__chatHistory.Add(role='assistant', message=__response.response)   # Añade la respuesta al historial.
                self.__print_response_info(response=__response)     # Imprime la información.
                print(f"🤖 (Robotico): {__response.response}")      # Imprime la respuesta.
                print()                 # Imprime salto de línea.
                
        # Si se detecta un Ctrl+C.
        except KeyboardInterrupt:
            print()     # Imprime salto de línea.
            self.__logger.info("Ctrl+C detectado. Finalizada sesión de chat.")  # Imprime información.
        # Si se detecta otra excepción.
        except Exception as e:
            self.__logger.error(f"Se ha detectado un error. ERROR: {e}")        # Imprime información.