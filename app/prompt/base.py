
# ---- MÓDULOS ---- #
from abc import ABC, abstractmethod
from typing import List, Dict

# ---- CLASES ---- #
class PromptStrategy(ABC):
    """
    Interfaz para las distintass estrategias de generación de prompts.
    """
    # -- Métodos -- #
    @abstractmethod
    def build_prompt(self, user_input:str, history:List[Dict[str, str]]):
        """
        Construye el prompt final a partir del input del usuario.
        
        Args:
            user_input (str): Entrada del usuario.
            history (List[Dict[str, str]]): Historial del chat.
        """
        pass