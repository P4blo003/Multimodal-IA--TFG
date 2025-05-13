

# ---- MÓDULOS ---- #
from ollama.client import OllamaClient
from ollama.response import Response

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
        self.__exitCommands:list[str] = ["EXIT", "QUIT", "SALIR"]
    
    # -- Métodos públicos -- #
    def Start(self) -> None:
        """
        Inicia el bucle de chat. Solicita entradas al usuario y muestra respuestas del modelo.
        Finaliza cuando el usuario escribe una palabra de salida.
        """
        # Búcle infinito para el chat.
        while True:
            prompt = input("🧠 Usuario: ")          # Obtiene el mensaje del usuario.
            # Si el mensaje del usuario es un mensaje de salida.
            if prompt.upper().strip() in CONFIG.chat.exitCommands:
                break                       # Finaliza el búcle.
            
            # Envía y recibe el mensaje del modelo.
            reply:Response = self.__client.send_message(message=prompt)
            # Si se ha recibido una respuesta.
            if reply:
                print(f"🤖 {reply.model}: {reply.response}")                    # Imprime la respuesta.
            # Si no se ha recibido una respuesta.
            else:
                print(f"⚠️ Advertencia: no se pudo recibir ningún mensaje.")    # Imprime el mensaje.