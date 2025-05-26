
# ---- MÓDULOS ---- #
from backend.manager import BackendManager
from chat.history import ChatHistory

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from config.context import CFG

# ---- CLASES ---- #
class LangChainManager(BackendManager):
    """
    Instancia que extiende `BackendManager` y se configura para emplear el módulo de
    `LangChain`.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la instancia.
        """
        super().__init__()      # Constructor de BackendManager.
        

    # -- Métodos BackendManager -- #
    def BuildPrompt(self, user_input:str, history:ChatHistory) -> str:
        """
        Construye el prompt a partir del contexto, historial y query.
        
        Args:
            user_input (str): Input del usuario.
            history (ChatHistory): Historial del chat.
            
        Returns:
            str: El prompt construido.
        """
        pass