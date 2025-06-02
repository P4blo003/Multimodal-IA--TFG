

# ---- MÓDULOS ---- #
from .session import ChatSession
from model.response import Response

from .rag.backend import BaseBackend, HaystackBackend, LangChainBackend

from service.ollama_service import OllamaService

from config.schema import ServerConfig


# ---- CLASES ---- #
class ConversationController:
    """
    Clase que se encarga de gestionar la conversación del cliente con el modelo. Gestiona el RAG,
    genera el prompt en función de la sesión y obtiene la respuesta del modelo.
    """
    # -- Métodos por defecto -- #
    def __init__(self, cfg:ServerConfig):
        """
        Inicializa la instancia.
        
        Args:
            cfg (ServerConfig): Configuración del servidor.
        """
        # Inicializa las propiedades.
        match (cfg.rag.backend):
            case 'HAYSTACK':
                self.__backend:BaseBackend = HaystackBackend()
            case 'LANGCHAIN':
                self.__backend:BaseBackend = LangChainBackend()
    
    
    # -- Métodos públicos -- #
    def get_response(self, query:str, session:ChatSession) -> Response:
        """
        Gestiona el Rag, genera el prompt, lo envía a la API de Ollama y retorna la respuesta.
        
        Args:
            query (str): La query del usuario.
            session (ChatSession): Session del chat.
        
        Returns:
            Response: La respuesta generada.
        """
        # Genera el prompt.
        prompt:str = self.__backend.BuildPrompt(user_input=query, session=session)

        # Retorna la respuesta obtenida.
        return OllamaService.get_response(prompt=prompt)