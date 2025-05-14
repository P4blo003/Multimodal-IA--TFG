# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/utils/log/logger.py
# Autor: Pablo González García
# Descripción:
# Módulo con clases y funciones encargadas de gestionar la sesión
# del cliente con el modelo de Ollama.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from ollama.client import OllamaClient
from ollama.response import Response

from prompt.base import PromptStrategy
from prompt.jinja import JinjaPrompt

from ollama.chat import ChatHistory

from config.context import CONFIG

# ---- CLASES ---- #
class ChatSession:
    """
    Clase que gestiona una sesión de chat simple con un modelo LLM local a través 
    de Ollama.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la sesión de chat con un modelo Ollama dado.
        """
        self.__client:OllamaClient = OllamaClient()  # Inicializa el cliente de Ollama.
        self.__chatHistory:ChatHistory = ChatHistory(CONFIG.ollama.historyMaxSize)                  # Inicializa el historial de mensajes.
        self.__promtpStrategy:PromptStrategy = JinjaPrompt()    # Inicializa la estrategia de prompting.
    
    # -- Métodos públicos -- #
    def Start(self) -> None:
        """
        Inicia el bucle de chat. Solicita entradas al usuario y muestra respuestas del modelo.
        Finaliza cuando el usuario escribe una palabra de salida.
        """
        # Búcle infinito para el chat.
        while True:
            user_input = input("🧠 Usuario: ")          # Obtiene el mensaje del usuario.
            # Si el mensaje del usuario es un mensaje de salida.
            if user_input.upper().strip() in CONFIG.chat.exitCommands:
                break                       # Finaliza el búcle.
            
            # Añade el mensaje al historial.
            self.__chatHistory.add_message(role="user", message=user_input)
            # Genera el prompt.
            prompt:str = self.__promtpStrategy.build_prompt(user_input=user_input, history=self.__chatHistory.Messages)
            # Envía y recibe el mensaje del modelo.
            reply:Response = self.__client.send_message(prompt=prompt)
            # Si se ha recibido una respuesta.
            if reply:
                print(f"🤖 {reply.model}: {reply.response}")                    # Imprime la respuesta.
                # Añade el mensaje al historial.
                self.__chatHistory.add_message(role="assistant", message=reply.response)
            # Si no se ha recibido una respuesta.
            else:
                print(f"⚠️ Advertencia: no se pudo recibir ningún mensaje.")    # Imprime el mensaje.